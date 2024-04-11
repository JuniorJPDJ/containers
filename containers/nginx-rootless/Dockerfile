# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nginx extractVersion=^(?<version>.*)-alpine$
# app_version: 1.25.4
# revision: 1
# description: Nginx image modified to run without root privileges
FROM  nginx:1.25.4-alpine@sha256:31bad00311cb5eeb8a6648beadcf67277a175da89989f14727420a80e2e76742

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
