# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_24/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.5.0
# revision: 3
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.24.3@sha256:be2656061b536c1883c4034790e21d0a09c5aaaf51968b89368a3c0371ea2c9a

# renovate: datasource=repology depName=alpine_3_24/rsync versioning=loose
ARG   RSYNC_VERSION="3.5.0-r0"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
