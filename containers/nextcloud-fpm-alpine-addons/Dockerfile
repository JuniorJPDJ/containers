# platforms: linux/amd64,linux/arm64,linux/arm/v7,linux/386,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nextcloud extractVersion=^(?<version>.*)-fpm-alpine$
# app_version: 30.0.6
# revision: 1
# description: Nextcloud fpm alpine image with addons (imagemagick, smb support, imap support, kerberos support)
FROM  nextcloud:30.0.6-fpm-alpine@sha256:fd092d936643c2e0c0b80c27d5518c793e5e215d5b5836e5ecdca973395b2c34

# renovate: datasource=repology depName=alpine_3_21/ffmpeg versioning=loose
ARG   FFMPEG_VERSION="6.1.2-r1"
# renovate: datasource=repology depName=alpine_3_21/imagemagick versioning=loose
ARG   IMAGEMAGICK_VERSION="7.1.1.41-r0"
# renovate: datasource=repology depName=alpine_3_21/procps-ng versioning=loose
ARG   PROCPS_NG_VERSION="4.0.4-r2"
# renovate: datasource=repology depName=alpine_3_21/samba-client versioning=loose
ARG   SAMBA_CLIENT_VERSION="4.20.6-r1"
# renovate: datasource=repology depName=alpine_3_21/supervisor versioning=loose
ARG   SUPERVISOR_VERSION="4.2.5-r5"
# renovate: datasource=repology depName=alpine_3_21/imap-dev versioning=loose
ARG   IMAP_VERSION="2007f-r15"
# renovate: datasource=repology depName=alpine_3_21/krb5-dev versioning=loose
ARG   KRB5_VERSION="1.21.3-r0"
# renovate: datasource=repology depName=alpine_3_21/openssl-dev versioning=loose
ARG   OPENSSL_VERSION="3.3.3-r0"
# renovate: datasource=repology depName=alpine_3_21/bzip2-dev versioning=loose
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
