# platforms: linux/amd64,linux/arm64
FROM        alpine:3.19.1 AS patch
ARG         SYNCREPO_VERSION=4fe427a2

RUN         apk add --no-cache \
              patch && \

ADD         --chmod=755 \
              https://gitlab.archlinux.org/archlinux/infrastructure/-/raw/${SYNCREPO_VERSION}/roles/syncrepo/files/syncrepo-template.sh \
              /syncrepo
COPY        syncrepo.patch /

RUN         patch /syncrepo /syncrepo.patch


FROM        alpine:3.19.1

ENV         TARGETDIR=out
ENV         BWLIMIT=0
ENV         SOURCE_URL=
ENV         LAST_UPDATE_URL=

VOLUME      /var/mirror

RUN         apk add --no-cache \
              rsync curl bash && \
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
