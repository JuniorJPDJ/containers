#!/bin/bash
CONTAINER="$1"

df="containers/$CONTAINER/Dockerfile"

appver="$(grep "^# app_version:" "$df" | awk '{print $3}')"
prev_appver="$(git show "HEAD:$df" | grep "^# app_version:" | awk '{print $3}')"
rev="$(grep "^# revision:" "$df" | awk '{print $3}')"

if [ "$appver" != "$prev_appver" ] ; then
  # will not work when reverting version
  echo "app_version for $CONTAINER changed, reseting revision to 1"
  rev=1
else
  echo "bumping $CONTAINER revision"
  (( rev++ ))
fi

sed -i "s/^# revision:.*/# revision: ${rev}/g" "$df"
