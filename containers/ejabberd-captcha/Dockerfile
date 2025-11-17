# platforms: linux/amd64
# renovate: datasource=docker depName=ejabberd/ecs
# app_version: 25.10
# revision: 1
# description: Robust, Ubiquitous and Massively Scalable Messaging Platform (XMPP, MQTT, SIP Server) with captcha scripts support and replacement of placeholders in config file with environment variables
FROM        ejabberd/ecs:25.10@sha256:1a89851f05d3377d14cfec7b13aa9236c5487490b9169cda07e0ef6224f8b70a

# renovate: datasource=repology depName=alpine_3_22/imagemagick versioning=loose
ARG         IMAGEMAGICK_VERSION="7.1.2.8-r0"
# renovate: datasource=repology depName=alpine_3_22/ghostscript-fonts versioning=loose
ARG         GHOSTSCRIPT_FONTS_VERSION="8.11-r5"
# renovate: datasource=repology depName=alpine_3_22/bash versioning=loose
ARG         BASH_VERSION="5.2.37-r0"
# renovate: datasource=repology depName=alpine_3_22/gettext versioning=loose
ARG         GETTEXT_VERSION="0.24.1-r0"

USER        root

COPY        --chmod=755 \
              custom_entrypoint.sh /custom_entrypoint.sh

RUN         apk add --no-cache \
              imagemagick=${IMAGEMAGICK_VERSION} \
              ghostscript-fonts=${GHOSTSCRIPT_FONTS_VERSION} \
              bash=${BASH_VERSION} \
              gettext=${GETTEXT_VERSION}

USER        ejabberd

ENV         CAPTCHA_CMD="/home/ejabberd/bin/captcha-ng.sh"

ENTRYPOINT  ["/custom_entrypoint.sh", "/home/ejabberd/bin/ejabberdctl"]
CMD         ["foreground"]
