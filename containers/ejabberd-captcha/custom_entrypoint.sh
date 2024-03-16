#!/bin/sh

export CAPTCHA_CMD="$(echo /home/ejabberd/lib/ejabberd-*/priv/bin/captcha-ng.sh)"
export EJABBERD_CONFIG_PATH="/tmp/ejabberd.yml"

envsubst < /home/ejabberd/conf/ejabberd.yml > $EJABBERD_CONFIG_PATH

exec "$@"
