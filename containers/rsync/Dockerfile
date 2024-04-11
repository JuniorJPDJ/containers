# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_19/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.2.7
# revision: 4
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.19.1@sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672bd4f27761f8e1ad6b

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
