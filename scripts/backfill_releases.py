#!/usr/bin/env python3
"""One-off backfill: create GitHub releases for already-published container versions.

For every container in containers/ and every version tag (X.Y.Z-rN) found on the
registry, creates a GitHub release "<container>-v<version>" (title
"<container> v<version>") with notes generated from the git history of that
container's directory.

NOT wired into CI - safe to delete once the backfill has been run.
Idempotent: existing releases and existing remote tags are skipped, so the
script can be re-run after partial failures.

Usage:
    backfill_releases.py [--dry-run] [--container NAME] [--sample N] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REGISTRY = "ghcr.io"
CACHE_DIR = Path("/tmp/opencode/backfill-cache")
COMMIT_LIMIT = 30
VERSION_RE = re.compile(r"^\d+(?:\.\d+)*-r\d+$")
NOREPLY_EMAIL_RE = re.compile(r"^(?:\d+\+)?([A-Za-z0-9-]+)@users\.noreply\.github\.com$")
LOG_PRETTY = "%H%x00%h%x00%ae%x00%an%x00%s"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def run(cmd: list[str], *, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, **(env_extra or {})}
    return subprocess.run(cmd, text=True, capture_output=True, env=env)


def out(cmd: list[str], *, env_extra: dict[str, str] | None = None) -> str:
    """Run a command and return stripped stdout; raise on failure."""
    proc = run(cmd, env_extra=env_extra)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def sha_exists(sha: str) -> bool:
    return bool(sha) and run(["git", "cat-file", "-e", f"{sha}^{{commit}}"]).returncode == 0


def is_ancestor(prev: str, cur: str) -> bool:
    return run(["git", "merge-base", "--is-ancestor", prev, cur]).returncode == 0


def short(sha: str) -> str:
    return sha[:12]


def version_key(version: str) -> tuple[int, ...]:
    """'1.2.3-r7' -> (1, 2, 3, 7) for version sorting."""
    base, _, rev = version.partition("-r")
    parts = [int(p) for p in base.split(".")]
    return tuple(parts + [0] * (3 - len(parts)) + [int(rev)])


# ---------------------------------------------------------------------------
# Repo context
# ---------------------------------------------------------------------------
def repo_slug() -> str:
    url = out(["git", "remote", "get-url", "origin"])
    match = re.search(r"github\.com[:/](.+?)(?:\.git)?/?$", url)
    if not match:
        sys.exit(f"Cannot parse github repo from origin: {url}")
    return match.group(1)


REPO = repo_slug()
REPO_URL = f"https://github.com/{REPO}"
NS = REPO.split("/")[0].lower()
IMAGE_BASE = f"{REGISTRY}/{NS}/{REPO.split('/')[1]}"


# ---------------------------------------------------------------------------
# Author resolution: git email -> GitHub @handle
# ---------------------------------------------------------------------------
class AuthorResolver:
    """Caches one resolution per author email.

    Tier 1: noreply email embeds the handle        -> free
    Tier 2: gh api commit lookup (.author.login)   -> one call per unique email
    Tier 3: plain git author name (no @)           -> free fallback
    """

    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def resolve(self, email: str, name: str, sha: str) -> str:
        if email not in self.cache:
            handle = NOREPLY_EMAIL_RE.match(email)
            if handle:
                self.cache[email] = f"@{handle.group(1)}"
            else:
                login = None
                try:
                    login = out(["gh", "api", f"repos/{REPO}/commits/{sha}",
                                 "-q", ".author.login // empty"])
                except RuntimeError as err:
                    print(f"    author lookup failed for {sha}: {err}")
                self.cache[email] = f"@{login}" if login else name
        return self.cache[email]


# ---------------------------------------------------------------------------
# Registry access (crane), with a config-blob cache
# ---------------------------------------------------------------------------
@dataclass
class Version:
    version: str
    created: str
    sha: str


def crane_config(image: str) -> dict:
    cache_file = CACHE_DIR / (re.sub(r"[^A-Za-z0-9._-]", "_", image) + ".json")
    if not cache_file.is_file() or cache_file.stat().st_size == 0:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        proc = run(["crane", "config", image])
        if proc.returncode != 0:
            cache_file.unlink(missing_ok=True)
            raise RuntimeError(f"crane config {image}: {proc.stderr.strip()}")
        cache_file.write_text(proc.stdout)
    return json.loads(cache_file.read_text())


def registry_versions(image_base: str, container: str) -> list[Version]:
    """List published X.Y.Z-rN tags with build date + commit SHA from labels."""
    try:
        tags = out(["crane", "ls", f"{image_base}/{container}"]).split()
    except RuntimeError as err:
        print(f"  crane ls failed, treating as no versions: {err}")
        return []
    versions = sorted({t for t in tags if VERSION_RE.match(t)})
    result: list[Version] = []
    total = len(versions)
    for i, version in enumerate(versions, 1):
        print(f"  [{i:3d}/{total:3d}] {version}: ", end="", flush=True)
        try:
            cfg = crane_config(f"{image_base}/{container}:{version}")
            created = cfg.get("created") or ""
            sha = (cfg.get("config", {}).get("Labels") or {}).get(
                "org.opencontainers.image.revision", "")
            print("ok")
        except RuntimeError:
            created, sha = "", ""
            print("config FAILED")
        result.append(Version(version, created or "1970-01-01T00:00:00Z", sha))
    result.sort(key=lambda v: (v.created, version_key(v.version)))
    return result


# ---------------------------------------------------------------------------
# GitHub state
# ---------------------------------------------------------------------------
def existing_release_tags() -> set[str]:
    return set(out(["gh", "api", "repos/{}/releases?per_page=100".format(REPO),
                    "--paginate", "-q", ".[].tag_name"]).split())


def existing_git_tags() -> set[str]:
    tags: set[str] = set()
    for line in out(["git", "ls-remote", "--tags", "origin"]).splitlines():
        ref = line.split("\t", 1)[-1]
        if ref.startswith("refs/tags/") and not ref.endswith("^{}"):
            tags.add(ref.removeprefix("refs/tags/"))
    return tags


@dataclass
class Commit:
    full: str
    short: str
    email: str
    name: str
    subject: str


def commits_since(prev_sha: str, cur_sha: str, container: str) -> list[Commit]:
    proc = run(["git", "log", f"--pretty={LOG_PRETTY}", f"{prev_sha}..{cur_sha}",
                "--", f"containers/{container}"])
    commits: list[Commit] = []
    for line in proc.stdout.splitlines():
        parts = line.split("\x00")
        if len(parts) == 5:
            commits.append(Commit(*parts))
    return commits


# ---------------------------------------------------------------------------
# Release body
# ---------------------------------------------------------------------------
@dataclass
class BodyResult:
    text: str
    fallback: bool = False
    no_changelog_reason: str | None = None
    reason: str = ""


def build_body(container: str, version: Version, prev_tag: str | None,
               resolver: AuthorResolver) -> BodyResult:
    sha = version.sha
    tag = f"{container}-v{version.version}"
    lines: list[str] = []
    result = BodyResult(text="")

    if prev_tag is None:
        result.no_changelog_reason = "initial release"
        lines += [f"Initial release of the `{container}` container.", ""]
        if sha_exists(sha):
            lines.append(f"**Built from**: {REPO_URL}/commit/{short(sha)}")
        else:
            # No usable content for the body - keep it empty, log the reason.
            result.fallback = True
            result.reason = "build commit missing from git history"
            result.no_changelog_reason = result.reason
            lines = []
    else:
        prev_sha = ""
        if sha_exists(sha):
            proc = run(["git", "rev-parse", "-q", "--verify", f"{prev_tag}^{{commit}}"])
            prev_sha = proc.stdout.strip() if proc.returncode == 0 else ""
        if not sha_exists(sha):
            result.reason = "build commit missing from git history"
        elif not prev_sha:
            result.reason = f"previous release tag {prev_tag} not found in git history"
        elif not is_ancestor(prev_sha, sha):
            result.reason = "rebuilt from a commit outside master lineage (no commit range)"

        if result.reason:
            result.fallback = True
            result.no_changelog_reason = result.reason
            # Reason stays in the logs only - body is just the provenance link.
            if sha_exists(sha):
                lines.append(f"**Built from**: {REPO_URL}/commit/{short(sha)}")
        else:
            commits = commits_since(prev_sha, sha, container)
            if commits:
                lines += ["## What's Changed", ""]
                shown = commits[:COMMIT_LIMIT]
                for c in shown:
                    author = resolver.resolve(c.email, c.name, c.full)
                    url = f"{REPO_URL}/commit/{c.full}"
                    lines.append(f"* {c.subject} by {author} in [{c.short}]({url})")
                if len(commits) > COMMIT_LIMIT:
                    lines.append(f"... and {len(commits) - COMMIT_LIMIT} more")
                lines.append("")
            else:
                lines += ["No container-specific commits in this range "
                          "(base image update or rebuild).", ""]
            lines.append(f"**Full Changelog**: "
                         f"{REPO_URL}/compare/{prev_tag}...{tag}")

    result.text = "\n".join(lines).rstrip() + "\n"
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--container")
    parser.add_argument("--sample", type=int, default=0,
                        help="dry-run: print N full bodies per container")
    parser.add_argument("--verbose", action="store_true",
                        help="print full body for every version")
    args = parser.parse_args()

    resolver = AuthorResolver()
    print(f"repo:     {REPO}\nimages:   {IMAGE_BASE}/<container>")
    print("mode:     " + ("DRY-RUN" if args.dry_run else "LIVE") + "\n")

    token = os.environ.get("GH_TOKEN") or run(["gh", "auth", "token"]).stdout.strip()
    if token:
        proc = subprocess.run(["crane", "auth", "login", REGISTRY, "-u", REPO.split("/")[0],
                               "--password-stdin"], input=token, text=True, capture_output=True)
        if proc.returncode == 0:
            print(f"crane: authenticated as {REPO.split('/')[0]}")
        else:
            print("crane: token login failed, continuing anonymously")

    print("fetching existing releases...")
    releases = existing_release_tags()
    print(f"found {len(releases)} existing releases")
    git_tags = existing_git_tags()
    print(f"found {len(git_tags)} existing git tags\n")

    totals = {"created": 0, "skipped": 0, "fallback": 0, "errors": 0}

    for path in sorted(Path("containers").iterdir()):
        container = path.name
        if not (path / "Dockerfile").is_file():
            continue
        if args.container and container != args.container:
            continue

        print(f"== {container}")
        versions = registry_versions(IMAGE_BASE, container)
        if not versions:
            print("   no version tags found, skipping\n")
            continue

        # Pass 0 (live): backdated annotated tags, batch-pushed per container.
        if not args.dry_run:
            to_push: list[str] = []
            for v in versions:
                tag = f"{container}-v{v.version}"
                if tag in releases or tag in git_tags:
                    continue
                if not sha_exists(v.sha):
                    continue
                date = v.created.partition(".")[0]
                proc = run(["git", "tag", "-f", "-a", tag, v.sha, "-m",
                            f"{container} {v.version}"],
                           env_extra={"GIT_COMMITTER_DATE": f"{date} +0000"})
                if proc.returncode != 0:
                    print(f"  ERROR creating tag {tag}: {proc.stderr.strip()}")
                    continue
                git_tags.add(tag)
                to_push.append(tag)
            if to_push:
                print(f"  pushing {len(to_push)} backdated tags...")
                proc = run(["git", "push", "origin", *to_push])
                if proc.returncode != 0:
                    print(f"  ERROR pushing tags for {container}: {proc.stderr.strip()}")
                else:
                    first = to_push[0]
                    tagger = out(["git", "cat-file", "-p", first]).split("tagger ", 1)[-1]
                    print(f"  tagger check: tagger {tagger}")

        prev_tag: str | None = None
        prev_sha = ""
        shown = 0
        counts = {"created": 0, "skipped": 0, "fallback": 0, "errors": 0}

        for v in versions:
            tag = f"{container}-v{v.version}"
            title = f"{container} v{v.version}"
            if tag in releases:
                counts["skipped"] += 1
                totals["skipped"] += 1
                print(f"  {tag}: release exists, skipping")
                prev_tag, prev_sha = tag, v.sha
                continue

            body = build_body(container, v, prev_tag, resolver)
            if body.fallback:
                counts["fallback"] += 1
                totals["fallback"] += 1

            status_extra = ""
            if body.fallback:
                status_extra += f" [FALLBACK: {body.reason}]"
            if body.no_changelog_reason:
                status_extra += f" [no changelog link: {body.no_changelog_reason}]"

            if args.dry_run:
                print(f"  [dry] would create {tag} (tag date {v.created.partition('.')[0]}, "
                      f"target {short(v.sha)}){status_extra}")
                if args.verbose or shown < args.sample:
                    shown += 1
                    print("  ----- body -----")
                    print("\n".join("  | " + l for l in body.text.splitlines()))
                    print("  ----------------")
            else:
                notes = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
                notes.write(body.text)
                notes.close()
                proc = run(["gh", "release", "create", tag, "--title", title,
                            "--notes-file", notes.name])
                Path(notes.name).unlink()
                if proc.returncode != 0:
                    counts["errors"] += 1
                    totals["errors"] += 1
                    print(f"  ERROR creating {tag}: {proc.stderr.strip()}")
                else:
                    counts["created"] += 1
                    totals["created"] += 1
                    releases.add(tag)
                    print(f"  created {tag}{status_extra}")

            prev_tag, prev_sha = tag, v.sha

        print("   summary: " + ", ".join(f"{k}={counts[k]}" for k in totals) + "\n")

    print("===================================================")
    print("TOTAL: " + ", ".join(f"{k}={totals[k]}" for k in totals))
    if args.dry_run:
        print("(dry run - nothing was created)")


if __name__ == "__main__":
    main()
