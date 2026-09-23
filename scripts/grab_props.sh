#!/bin/bash
GIT_DIFF_ENABLED="$1"
GIT_DIFF_BASE="$2"
GIT_DIFF_HEAD="$3"
SKIP_UNBUMPED="${4:-0}"


cd containers

NO_CONTAINERS=1
for d in * ; do
  # check if directory changed and skip if not
  [ "$GIT_DIFF_ENABLED" = "1" ] && \
    git diff -s --exit-code "${GIT_DIFF_BASE}..${GIT_DIFF_HEAD}" -- "$d" && \
    continue

  df="$d/Dockerfile"
  if [ -f "$df" ] ; then
    PUSH="true"

    if [ "$GIT_DIFF_ENABLED" = "1" -a "$SKIP_UNBUMPED" = "1" ] ; then
      base_appver="$(git show "$GIT_DIFF_BASE:./$df" 2>/dev/null | grep "^# app_version:" | awk '{print $3}')"
      head_appver="$(git show "$GIT_DIFF_HEAD:./$df" 2>/dev/null | grep "^# app_version:" | awk '{print $3}')"
      base_rev="$(git show "$GIT_DIFF_BASE:./$df" 2>/dev/null | grep "^# revision:" | awk '{print $3}')"
      head_rev="$(git show "$GIT_DIFF_HEAD:./$df" 2>/dev/null | grep "^# revision:" | awk '{print $3}')"

      if [ "$base_appver" == "$head_appver" -a "$base_rev" == "$head_rev" ] ; then
        echo "[Container $d]: app_version and revision unchanged ($head_appver-r$head_rev), will build without pushing"
        PUSH="false"
      fi
    fi

    echo "- \"container\": \"$d\""
    echo "  \"push\": \"$PUSH\""
    # extract additional properties from Dockerfiles
    sed -En 's/^#\s+((\w|-)+):\s+(.+)$/  "\1": "\3"/p' "$df" | grep -v '"renovate":'
    NO_CONTAINERS=0
  fi

done

[ $NO_CONTAINERS = 1 ] && echo '[]'
