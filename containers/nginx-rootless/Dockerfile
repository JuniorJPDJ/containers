# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nginx extractVersion=^(?<version>.*)-alpine$
# app_version: 1.27.0
# revision: 2
# description: Nginx image modified to run without root privileges
FROM  nginx:1.27.0-alpine@sha256:5c0c2272256857e486cf9fe2983db41c0e14c72476f5ebedf474289fd9ca8627

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
