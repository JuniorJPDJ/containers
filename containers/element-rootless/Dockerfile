# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=vectorim/element-web extractVersion=^v(?<version>.*)$
# app_version: 1.11.81
# revision: 1
# description: Matrix Element Web client modified to run without root privileges
FROM  vectorim/element-web:v1.11.81@sha256:6831fb2e55e16b0dfd0ef349001066393402a8d56ea05ea85af6244de48ba71c

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
