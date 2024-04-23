# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=vectorim/element-web extractVersion=^v(?<version>.*)$
# app_version: 1.11.65
# revision: 1
# description: Matrix Element Web client modified to run without root privileges
FROM  vectorim/element-web:v1.11.65@sha256:abbd2bf6825548db7838ebf16e72dfe55f460eb6111b36bcd8dbdb85762c0a87

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
