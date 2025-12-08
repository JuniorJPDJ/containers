# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_23/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.34.2
# revision: 1
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.23.0@sha256:51183f2cfa6320055da30872f211093f9ff1d3cf06f39a0bdb212314c5dc7375

# renovate: datasource=repology depName=alpine_3_23/openssl versioning=loose
ARG   OPENSSL_VERSION="3.5.4-r0"
# renovate: datasource=repology depName=alpine_3_23/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.34.2-r1"
# renovate: datasource=repology depName=alpine_3_23/jq versioning=loose
ARG   JQ_VERSION="1.8.1-r0"
# renovate: datasource=repology depName=alpine_3_23/yq-go versioning=loose
ARG   YQ_VERSION="4.49.2-r1"
# renovate: datasource=repology depName=alpine_3_23/bash versioning=loose
ARG   BASH_VERSION="5.3.3-r1"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
        bash=${BASH_VERSION} \
      && \
      rm -rf /var/cache/apk/*
