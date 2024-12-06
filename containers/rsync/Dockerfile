# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_21/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.3.0
# revision: 7
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.21.0@sha256:21dc6063fd678b478f57c0e13f47560d0ea4eeba26dfc947b2a4f81f686b9f45

# renovate: datasource=repology depName=alpine_3_21/rsync versioning=loose
ARG   RSYNC_VERSION="3.3.0-r1"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
