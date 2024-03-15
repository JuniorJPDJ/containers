#!/bin/sh

cd /etc/letsencrypt/live/
out=/etc/certs

for dir in *
do
    if [ ! -d $dir ]; then
      continue
    fi

    echo "Copying $dir"
    mkdir -p $out/$dir
    cp -L $dir/*.pem $out/$dir/
    cat $dir/fullchain.pem $dir/privkey.pem > $out/$dir/haproxy_full.pem
    chmod +r $out/$dir/*
done

