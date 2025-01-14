# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=vectorim/element-web extractVersion=^v(?<version>.*)$
# app_version: 1.11.90
# revision: 1
# description: Matrix Element Web client modified to run without root privileges
FROM  vectorim/element-web:v1.11.90@sha256:953b93ff9036e1af89044c5538c4b2ecbf287f1319122786ea37c7c8a2a1fe85

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
