# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=vectorim/element-web extractVersion=^v(?<version>.*)$
# app_version: 1.11.71
# revision: 1
# description: Matrix Element Web client modified to run without root privileges
FROM  vectorim/element-web:v1.11.71@sha256:36b79b6113324b1977c71a643fbf86a00959c770a8413c8808ac5c66b74c2a7d

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
