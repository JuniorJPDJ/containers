# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_21/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.31.3
# revision: 4
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.21.2@sha256:56fa17d2a7e7f168a043a2712e63aed1f8543aeafdcee47c58dcffe38ed51099

# renovate: datasource=repology depName=alpine_3_21/openssl versioning=loose
ARG   OPENSSL_VERSION="3.3.2-r5"
# renovate: datasource=repology depName=alpine_3_21/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.31.3-r1"
# renovate: datasource=repology depName=alpine_3_21/jq versioning=loose
ARG   JQ_VERSION="1.7.1-r0"
# renovate: datasource=repology depName=alpine_3_21/yq-go versioning=loose
ARG   YQ_VERSION="4.44.5-r1"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
      && \
      rm -rf /var/cache/apk/*
