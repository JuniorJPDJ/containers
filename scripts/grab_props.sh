#!/bin/bash
GIT_DIFF_ENABLED=$1
GIT_DIFF_BASE=$2
GIT_DIFF_HEAD=$3


cd containers

NO_CONTAINERS=1
for d in * ; do
  # check if directory changed and skip if not
  [ "$GIT_DIFF_ENABLED" = "1" ] && \
    git diff -s --exit-code "${GIT_DIFF_BASE}..${GIT_DIFF_HEAD}" "$d" && \
    continue

  if [ -f "$d/Dockerfile" ] ; then
    echo "- container: \"$d\""
    # extract additional properties from Dockerfiles
    sed -En 's/^#\s+((\w|-)+):\s+(.+)$/  "\1": "\3"/p' "$d/Dockerfile"
    NO_CONTAINERS=0
  fi

done

[ $NO_CONTAINERS = 1 ] && echo '[]'
