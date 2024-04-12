#!/bin/bash
GIT_DIFF_BASE="$1"
GIT_DIFF_HEAD="$2"
EXIT_CODE=0
CHANGED=0

[ -z "$GIT_DIFF_BASE" -o -z "$GIT_DIFF_HEAD" ] &&
  echo "GIT_DIFF_BASE or GIT_DIFF_HEAD not provided. Exiting." &&
  exit 1

cd containers

for d in * ; do
  # check if directory changed and skip if not
  git diff -s --exit-code "${GIT_DIFF_BASE}..${GIT_DIFF_HEAD}" "$d" && \
    continue
  CHANGED=1
  echo "[Container $d]: files changed, checking versions"

  df="./$d/Dockerfile"
  if [ -f "$df" ] ; then
    base_appver="$(git show "$GIT_DIFF_BASE:$df" | grep "^# app_version:" | awk '{print $3}')"
    echo "[Container $d]: base app_version: $base_appver"
    head_appver="$(git show "$GIT_DIFF_HEAD:$df" | grep "^# app_version:" | awk '{print $3}')"
    echo "[Container $d]: head app_version: $head_appver"
    base_rev="$(git show "$GIT_DIFF_BASE:$df" | grep "^# revision:" | awk '{print $3}')"
    echo "[Container $d]: base revision: $base_rev"
    head_rev="$(git show "$GIT_DIFF_HEAD:$df" | grep "^# revision:" | awk '{print $3}')"
    echo "[Container $d]: head revision: $head_rev"

    if [ "$base_appver" == "$head_appver" -a "$base_rev" == "$head_rev" ] ; then
      echo -e "[Container $d]: \e[31mapp_version and revision not changed, this should be fixed!\e[0m"
      EXIT_CODE=2
    else
      echo -e "[Container $d]: \e[32mapp_version or revision changed, everything is ok!\e[0m"
    fi
  fi
done

[ "$CHANGED" == "0" ] && \
  echo -e "\e[32mNo container changes detected, everything is ok!\e[0m"
exit $EXIT_CODE
