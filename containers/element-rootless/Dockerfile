# platforms: linux/amd64,linux/arm64
FROM  vectorim/element-web:v1.11.62@sha256:5845a8112dd814ce6bd55700496c633cf5ca67484e97567cf9ce5e40776ea3e7

# make it run on non-root
RUN   mkdir -p /var/log/nginx /var/cache/nginx /var/run/nginx && \
      chown -R nginx:nginx /var/log/nginx /var/run/nginx /var/cache/nginx && \
      sed -e 's#/var/run/nginx.pid#/var/run/nginx/nginx.pid#' -i /etc/nginx/nginx.conf

USER  nginx
