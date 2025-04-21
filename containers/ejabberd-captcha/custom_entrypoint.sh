#!/bin/sh

export EJABBERD_CONFIG_PATH="/tmp/ejabberd.yml"

envsubst < /home/ejabberd/conf/ejabberd.yml > $EJABBERD_CONFIG_PATH

exec "$@"
