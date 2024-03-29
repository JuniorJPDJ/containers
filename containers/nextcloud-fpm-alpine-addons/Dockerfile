# platforms: linux/amd64,linux/arm64,linux/arm/v7,linux/arm/v6,linux/386,linux/ppc64le,linux/s390x
FROM  nextcloud:28.0.3-fpm-alpine@sha256:0e2edb26be9a34715380c0981ff155c3d565ef557f94df01ccf17169d608e2c1

# renovate: datasource=repology depName=alpine_3_19/ffmpeg versioning=loose
ARG   FFMPEG_VERSION="6.1.1-r0"
# renovate: datasource=repology depName=alpine_3_19/imagemagick versioning=loose
ARG   IMAGEMAGICK_VERSION="7.1.1.26-r0"
# renovate: datasource=repology depName=alpine_3_19/procps-ng versioning=loose
ARG   PROCPS_NG_VERSION="4.0.4-r0"
# renovate: datasource=repology depName=alpine_3_19/samba-client versioning=loose
ARG   SAMBA_CLIENT_VERSION="4.18.9-r0"
# renovate: datasource=repology depName=alpine_3_19/supervisor versioning=loose
ARG   SUPERVISOR_VERSION="4.2.5-r4"
# renovate: datasource=repology depName=alpine_3_19/imap-dev versioning=loose
ARG   IMAP_VERSION="2007f-r15"
# renovate: datasource=repology depName=alpine_3_19/krb5-dev versioning=loose
ARG   KRB5_VERSION="1.21.2-r0"
# renovate: datasource=repology depName=alpine_3_19/openssl-dev versioning=loose
ARG   OPENSSL_VERSION="3.1.4-r5"
# renovate: datasource=repology depName=alpine_3_19/bzip2-dev versioning=loose
ARG   BZIP2_VERSION="1.0.8-r6"


COPY  fpm.conf /usr/local/etc/php-fpm.d/z_nextcloud_fpm.conf
COPY  php.ini /usr/local/etc/php/conf.d/z_nextcloud_php.ini

RUN   set -ex; \
      apk add --no-cache \
        ffmpeg=${FFMPEG_VERSION} \
        imagemagick=${IMAGEMAGICK_VERSION} \
        procps-ng=${PROCPS_NG_VERSION} \
        samba-client=${SAMBA_CLIENT_VERSION} \
        supervisor=${SUPERVISOR_VERSION}

RUN   set -ex; \
      apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        imap-dev=${IMAP_VERSION} \
        krb5-dev=${KRB5_VERSION} \
        openssl-dev=${OPENSSL_VERSION} \
        samba-dev \
        bzip2-dev=${BZIP2_VERSION} \
      && \
      docker-php-ext-configure imap --with-kerberos --with-imap-ssl && \
      docker-php-ext-install \
        bz2 \
        imap \
      && \
      pecl install smbclient && \
      docker-php-ext-enable smbclient && \
      runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \
          | tr ',' '\n' \
          | sort -u \
          | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
      )" && \
      apk add --virtual .nextcloud-phpext-rundeps $runDeps && \
      apk del .build-deps
