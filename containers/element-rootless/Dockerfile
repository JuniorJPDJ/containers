# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=vectorim/element-web extractVersion=^v(?<version>.*)$
# app_version: 1.11.84
# revision: 1
# description: Matrix Element Web client modified to run without root privileges
FROM  vectorim/element-web:v1.11.84@sha256:fdda9d781782da10a6278283267ea75359a16c0dbc23bee493863496bd985c0a

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
