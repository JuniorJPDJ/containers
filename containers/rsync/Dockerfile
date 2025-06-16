# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 3.4.1
# revision: 1
# description: Rsync running in cron, with ability to be just used as rsync when running with overwritten command
FROM  alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715

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
