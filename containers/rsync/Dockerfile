#bump test
# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
FROM  alpine:3.19.1

# renovate: datasource=repology depName=alpine_3_19/rsync versioning=loose
ARG   RSYNC_VERSION="3.2.7-r4"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
