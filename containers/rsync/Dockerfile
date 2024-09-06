# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_19/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.3.0
# revision: 5
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.20.3@sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd1367effd16dc0d06d

# renovate: datasource=repology depName=alpine_3_20/rsync versioning=loose
ARG   RSYNC_VERSION="3.3.0-r0"


RUN   apk add --no-cache \
        rsync=${RSYNC_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      echo "nobody" > /etc/crontabs/cron.update

COPY  crontab /etc/crontabs/nobody

CMD   echo Starting cron && \
      /usr/sbin/crond -f
