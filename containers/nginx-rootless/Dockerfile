# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nginx extractVersion=^(?<version>.*)-alpine$
# app_version: 1.31.1
# revision: 1
# description: Nginx image modified to run without root privileges
FROM  nginx:1.31.1-alpine@sha256:8b1e78743a03dbb2c95171cc58639fef29abc8816598e27fb910ed2e621e589a

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx /etc/nginx && \
      sed -e 's#/run/nginx.pid#/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
