#!/usr/bin/env python3
"""Create the GitHub release for a freshly published container version.

Called by the Docker publish workflow (one invocation per built container,
after the multiarch image has been pushed) and safe to run manually.

Idempotent: exits 0 without changes if the release already exists.
Notes are generated from the git history of the container's directory since
the newest previous "<container>-v*" release tag.

Usage:
    create_release.py <container> <app_version> <revision> [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

COMMIT_LIMIT = 30
VERSION_RE = re.compile(r"^\d+(?:\.\d+)*-r\d+$")
NOREPLY_EMAIL_RE = re.compile(r"^(?:\d+\+)?([A-Za-z0-9-]+)@users\.noreply\.github\.com$")
LOG_PRETTY = "%H%x00%h%x00%ae%x00%an%x00%s"


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True)


def out(cmd: list[str]) -> str:
    """Run a command and return stripped stdout; raise on failure."""
    proc = run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def short(sha: str) -> str:
    return sha[:12]


def version_key(version: str) -> tuple[int, ...]:
    """'1.2.3-r7' -> (1, 2, 3, 7) for version sorting."""
    base, _, rev = version.partition("-r")
    parts = [int(p) for p in base.split(".")]
    return tuple(parts + [0] * (3 - len(parts)) + [int(rev)])


def repo_slug() -> str:
    url = out(["git", "remote", "get-url", "origin"])
    match = re.search(r"github\.com[:/](.+?)(?:\.git)?/?$", url)
    if not match:
        sys.exit(f"Cannot parse github repo from origin: {url}")
    return match.group(1)


REPO = repo_slug()
REPO_URL = f"https://github.com/{REPO}"


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
                    print(f"author lookup failed for {sha}: {err}")
                self.cache[email] = f"@{login}" if login else name
        return self.cache[email]


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
# Previous release lookup
# ---------------------------------------------------------------------------
def existing_release_tags() -> set[str]:
    return set(out(["gh", "api", f"repos/{REPO}/releases?per_page=100",
                    "--paginate", "-q", ".[].tag_name"]).split())


def find_prev_tag(container: str, current_tag: str, release_tags: set[str]) -> str | None:
    """Newest previous release tag for this container, by version order."""
    prefix = f"{container}-v"
    candidates = [t for t in release_tags
                  if t.startswith(prefix) and t != current_tag]
    if not candidates:
        return None

    def key(tag: str) -> tuple[int, ...]:
        return version_key(tag.removeprefix(prefix))

    return max(candidates, key=key)


# ---------------------------------------------------------------------------
# Release body
# ---------------------------------------------------------------------------
@dataclass
class BodyResult:
    text: str
    fallback: bool = False
    no_changelog_reason: str | None = None
    reason: str = ""


def build_body(container: str, version: str, sha: str, prev_tag: str | None,
               resolver: AuthorResolver) -> BodyResult:
    tag = f"{container}-v{version}"
    lines: list[str] = []
    result = BodyResult(text="")

    if prev_tag is None:
        result.no_changelog_reason = "initial release"
        lines += [f"Initial release of the `{container}` container.", "",
                  f"**Built from**: {REPO_URL}/commit/{short(sha)}"]
    else:
        prev_proc = run(["git", "rev-parse", "-q", "--verify", f"{prev_tag}^{{commit}}"])
        prev_sha = prev_proc.stdout.strip() if prev_proc.returncode == 0 else ""

        if not prev_sha:
            result.reason = f"previous release tag {prev_tag} not found in git history"
        elif not is_ancestor(prev_sha, sha):
            result.reason = "rebuilt from a commit outside master lineage (no commit range)"

        if result.reason:
            # Reason stays in the logs only - body is just the provenance link.
            result.fallback = True
            result.no_changelog_reason = result.reason
            lines.append(f"**Built from**: {REPO_URL}/commit/{short(sha)}")
        else:
            commits = commits_since(prev_sha, sha, container)
            if commits:
                lines += ["## What's Changed", ""]
                for c in commits[:COMMIT_LIMIT]:
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


def is_ancestor(prev: str, cur: str) -> bool:
    return run(["git", "merge-base", "--is-ancestor", prev, cur]).returncode == 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("container")
    parser.add_argument("app_version")
    parser.add_argument("revision")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    version = f"{args.app_version}-r{args.revision}"
    if not VERSION_RE.match(version):
        sys.exit(f"Unexpected version format: '{version}' "
                 f"(from app_version='{args.app_version}' revision='{args.revision}')")
    tag = f"{args.container}-v{version}"
    sha = out(["git", "rev-parse", "HEAD"])

    if gh_release_exists(tag):
        print(f"release {tag} already exists, skipping")
        return

    release_tags = existing_release_tags()
    prev_tag = find_prev_tag(args.container, tag, release_tags)
    resolver = AuthorResolver()
    body = build_body(args.container, version, sha, prev_tag, resolver)

    status_extra = ""
    if body.fallback:
        status_extra += f" [FALLBACK: {body.reason}]"
    if body.no_changelog_reason:
        status_extra += f" [no changelog link: {body.no_changelog_reason}]"

    if args.dry_run:
        print(f"[dry] would create {tag} (target {short(sha)}, "
              f"prev: {prev_tag or 'none'}){status_extra}")
        print(body.text, end="")
        return

    notes = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    notes.write(body.text)
    notes.close()
    try:
        proc = run(["gh", "release", "create", tag, "--target", sha,
                    "--title", f"{args.container} v{version}",
                    "--notes-file", notes.name])
    finally:
        Path(notes.name).unlink()
    if proc.returncode != 0:
        sys.exit(f"ERROR creating {tag}: {proc.stderr.strip()}")
    print(f"created {tag}{status_extra}")


def gh_release_exists(tag: str) -> bool:
    return run(["gh", "api", f"repos/{REPO}/releases/tags/{tag}"]).returncode == 0


if __name__ == "__main__":
    main()
