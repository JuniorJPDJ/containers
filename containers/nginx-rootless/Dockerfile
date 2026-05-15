# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nginx extractVersion=^(?<version>.*)-alpine$
# app_version: 1.31.0
# revision: 2
# description: Nginx image modified to run without root privileges
FROM  nginx:1.31.0-alpine@sha256:dc48b7a872a79fb541ba5081d320b11b549231bc63ba465a7495afaa7d2ebcb8

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
      sed -e 's#/run/nginx.pid#/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
