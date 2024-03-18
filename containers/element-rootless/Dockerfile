# platforms: linux/amd64,linux/arm64
FROM  vectorim/element-web:v1.11.61@sha256:c689ef6b4c17038f683b626ad8d052cad69e826b0cf007d417621fc99fdb455e

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
