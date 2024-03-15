#!/bin/sh

mkdir -p /etc/letsencrypt/renewal-hooks/post/
ln -sf /opt/cp_certs.sh /etc/letsencrypt/renewal-hooks/post/cp_certs.sh
if [ $# -eq 0 ] ; then
  exec crond -f -d 8
fi

exec certbot "$@"
