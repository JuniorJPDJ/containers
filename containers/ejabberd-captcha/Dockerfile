# platforms: linux/amd64
# renovate: datasource=docker depName=ejabberd/ecs
# app_version: 25.07
# revision: 1
# description: Robust, Ubiquitous and Massively Scalable Messaging Platform (XMPP, MQTT, SIP Server) with captcha scripts support and replacement of placeholders in config file with environment variables
FROM        ejabberd/ecs:25.07@sha256:ddfc5e5f2c660fe605a4ddeec93b13c944380498f50417531475be984fd78d33

# renovate: datasource=repology depName=alpine_3_19/imagemagick versioning=loose
ARG         IMAGEMAGICK_VERSION="7.1.1.32-r0"
# renovate: datasource=repology depName=alpine_3_19/ghostscript-fonts versioning=loose
ARG         GHOSTSCRIPT_FONTS_VERSION="8.11-r5"
# renovate: datasource=repology depName=alpine_3_19/bash versioning=loose
ARG         BASH_VERSION="5.2.21-r0"
# renovate: datasource=repology depName=alpine_3_19/gettext versioning=loose
ARG         GETTEXT_VERSION="0.22.3-r0"

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
