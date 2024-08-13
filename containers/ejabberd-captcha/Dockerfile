# platforms: linux/amd64
# renovate: datasource=docker depName=ejabberd/ecs
# app_version: 24.07
# revision: 2
# description: Robust, Ubiquitous and Massively Scalable Messaging Platform (XMPP, MQTT, SIP Server) with captcha scripts support and replacement of placeholders in config file with environment variables
FROM        ejabberd/ecs:24.07@sha256:66718abc9817d7ff7afa5cda6b02e1b5263e451e12d5a1e3d0e0b0ed399fc2ae

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

ENTRYPOINT  ["/custom_entrypoint.sh", "/home/ejabberd/bin/ejabberdctl"]
CMD         ["foreground"]
