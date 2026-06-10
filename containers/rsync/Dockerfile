# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_23/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.4.3
# revision: 2
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.24.0@sha256:a2d49ea686c2adfe3c992e47dc3b5e7fa6e6b5055609400dc2acaeb241c829f4

# renovate: datasource=repology depName=alpine_3_23/rsync versioning=loose
ARG   RSYNC_VERSION="3.4.3-r0"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
