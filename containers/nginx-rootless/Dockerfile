# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nginx extractVersion=^(?<version>.*)-alpine$
# app_version: 1.29.5
# revision: 2
# description: Nginx image modified to run without root privileges
FROM  nginx:1.29.5-alpine@sha256:1eff5a5f3fcf8431a0abb7eddf5471fec24e5e1905a2581aeacdb07a4479b92b

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
      sed -e 's#/run/nginx.pid#/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
