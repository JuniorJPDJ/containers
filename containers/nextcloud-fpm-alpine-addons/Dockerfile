FROM nextcloud:26.0.12-fpm-alpine

COPY fpm.conf /usr/local/etc/php-fpm.d/z_nextcloud_fpm.conf
COPY php.ini /usr/local/etc/php/conf.d/z_nextcloud_php.ini

RUN set -ex; \
    \
    apk add --no-cache \
        ffmpeg \
        imagemagick \
        procps \
        samba-client \
        supervisor \
        libreoffice \
    ;

RUN set -ex; \
    \
    apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        imap-dev \
        krb5-dev \
        libretls-dev \
        samba-dev \
        bzip2-dev \
    && \
    \
    docker-php-ext-configure imap --with-kerberos --with-imap-ssl && \
    docker-php-ext-install \
        bz2 \
        imap \
    && \
    pecl install smbclient && \
    docker-php-ext-enable smbclient && \
    \
    runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \
            | tr ',' '\n' \
            | sort -u \
            | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
    )" && \
    apk add --virtual .nextcloud-phpext-rundeps $runDeps && \
    apk del .build-deps
