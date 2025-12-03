# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.4.1
# revision: 5
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.23.0@sha256:51183f2cfa6320055da30872f211093f9ff1d3cf06f39a0bdb212314c5dc7375

# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose
ARG   RSYNC_VERSION="3.4.1-r1"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
