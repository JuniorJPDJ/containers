# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_20/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.30.0
# revision: 11
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.20.2@sha256:0a4eaa0eecf5f8c050e5bba433f58c052be7587ee8af3e8b3910ef9ab5fbe9f5

# renovate: datasource=repology depName=alpine_3_20/openssl versioning=loose
ARG   OPENSSL_VERSION="3.3.1-r3"
# renovate: datasource=repology depName=alpine_3_20/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.30.0-r3"
# renovate: datasource=repology depName=alpine_3_20/jq versioning=loose
ARG   JQ_VERSION="1.7.1-r0"
# renovate: datasource=repology depName=alpine_3_20/yq-go versioning=loose
ARG   YQ_VERSION="4.44.1-r2"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
      && \
      rm -rf /var/cache/apk/*
