# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.4.1
# revision: 2
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.22.1@sha256:4bcff63911fcb4448bd4fdacec207030997caf25e9bea4045fa6c8c44de311d1

# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose
ARG   RSYNC_VERSION="3.4.1-r0"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
