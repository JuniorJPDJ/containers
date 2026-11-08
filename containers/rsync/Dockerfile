# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_24/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.5.2
# revision: 2
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.24.4@sha256:f59abe656b692d901e184be3445e084786602108599d2a51d229c0f5a48c71bf

# renovate: datasource=repology depName=alpine_3_24/rsync versioning=loose
ARG   RSYNC_VERSION="3.5.2-r1"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
