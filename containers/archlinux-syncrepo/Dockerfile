# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x
# app_version: 1.0.0
# revision: 24
# description: Arch Linux syncrepo mirror synchronization script
FROM        alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715 AS patch

ARG         SYNCREPO_VERSION=4fe427a2


RUN         apk add --no-cache \
              patch

ADD         --chmod=755 \
              https://gitlab.archlinux.org/archlinux/infrastructure/-/raw/${SYNCREPO_VERSION}/roles/syncrepo/files/syncrepo-template.sh \
              /syncrepo
COPY        syncrepo.patch /

RUN         patch /syncrepo /syncrepo.patch



FROM        alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715

# renovate: datasource=repology depName=alpine_3_22/rsync versioning=loose
ARG         RSYNC_VERSION="3.4.1-r0"
# renovate: datasource=repology depName=alpine_3_22/curl versioning=loose
ARG         CURL_VERSION="8.14.1-r0"
# renovate: datasource=repology depName=alpine_3_22/bash versioning=loose
ARG         BASH_VERSION="5.2.37-r0"


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
