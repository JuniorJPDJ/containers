# platforms: linux/amd64,linux/arm64,linux/arm/v7,linux/386,linux/ppc64le,linux/s390x
# renovate: datasource=docker depName=nextcloud extractVersion=^(?<version>.*)-fpm-alpine$
# app_version: 32.0.14
# revision: 4
# description: Nextcloud fpm alpine image with addons (ffmpeg, smb support, imap support, kerberos support)
FROM  nextcloud:32.0.14-fpm-alpine@sha256:da1d436568cd19d73f2a08d5f11c061e419a47f1be0f6ac29b53282086a85f58

# renovate: datasource=repology depName=alpine_3_24/ffmpeg versioning=loose
ARG   FFMPEG_VERSION="8.1.2-r0"
# renovate: datasource=repology depName=alpine_3_24/samba-client versioning=loose
ARG   SAMBA_VERSION="4.23.8-r0"
# renovate: datasource=repology depName=alpine_3_24/imap-dev versioning=loose
ARG   IMAP_VERSION="2007f-r16"
# renovate: datasource=repology depName=alpine_3_24/krb5-dev versioning=loose
ARG   KRB5_VERSION="1.22.2-r1"
# renovate: datasource=repology depName=alpine_3_24/openssl-dev versioning=loose
ARG   OPENSSL_VERSION="3.5.8-r0"


COPY  fpm.conf /usr/local/etc/php-fpm.d/z_nextcloud_fpm.conf
COPY  php.ini /usr/local/etc/php/conf.d/z_nextcloud_php.ini

RUN   set -ex; \
      apk add --no-cache \
        ffmpeg=${FFMPEG_VERSION} \
        samba-client=${SAMBA_VERSION}

RUN   set -ex; \
      apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        imap-dev=${IMAP_VERSION} \
        krb5-dev=${KRB5_VERSION} \
        openssl-dev=${OPENSSL_VERSION} \
        samba-dev=${SAMBA_VERSION} \
      && \
      docker-php-ext-configure imap --with-kerberos --with-imap-ssl && \
      docker-php-ext-install \
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
