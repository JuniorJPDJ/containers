#!/bin/ash

exec [ $(($(wget -O - -o /dev/null "$LAST_UPDATE_URL/../lastsync") - $(cat /var/mirror/$TARGETDIR/lastsync))) -lt 180 ]
