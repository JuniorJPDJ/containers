# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# app_version: 1.0.0
# revision: 5
# description: Arch Linux syncrepo mirror synchronization script
FROM        alpine:3.20.1@sha256:b89d9c93e9ed3597455c90a0b88a8bbb5cb7188438f70953fede212a0c4394e0 AS patch

ARG         SYNCREPO_VERSION=4fe427a2


RUN         apk add --no-cache \
              patch

ADD         --chmod=755 \
              https://gitlab.archlinux.org/archlinux/infrastructure/-/raw/${SYNCREPO_VERSION}/roles/syncrepo/files/syncrepo-template.sh \
              /syncrepo
COPY        syncrepo.patch /

RUN         patch /syncrepo /syncrepo.patch



FROM        alpine:3.20.1@sha256:b89d9c93e9ed3597455c90a0b88a8bbb5cb7188438f70953fede212a0c4394e0

# renovate: datasource=repology depName=alpine_3_20/rsync versioning=loose
ARG         RSYNC_VERSION="3.3.0-r0"
# renovate: datasource=repology depName=alpine_3_20/curl versioning=loose
ARG         CURL_VERSION="8.8.0-r0"
# renovate: datasource=repology depName=alpine_3_20/bash versioning=loose
ARG         BASH_VERSION="5.2.26-r0"


ENV         TARGETDIR=out
ENV         BWLIMIT=0
ENV         SOURCE_URL=
ENV         LAST_UPDATE_URL=

VOLUME      /var/mirror

RUN         apk add --no-cache \
              rsync=${RSYNC_VERSION} \
              curl=${CURL_VERSION} \
              bash=${BASH_VERSION} \
            && \
            rm -rf /var/cache/apk/* && \
            touch /var/lock/syncrepo.lck -t 0001010000 && \
            chmod 666 /var/lock/syncrepo.lck && \
            echo "nobody" > /etc/crontabs/cron.update

COPY        crontab /etc/crontabs/nobody
COPY        mirror_healthcheck.sh /bin/
COPY        --from=patch /syncrepo /bin/syncrepo

HEALTHCHECK CMD /bin/mirror_healthcheck.sh
CMD         mkdir -p "/var/mirror/$TARGETDIR" && \
            chown nobody "/var/mirror/$TARGETDIR" "/var/mirror/$TMPDIR" && \
            echo Starting cron && \
            /usr/sbin/crond -f
