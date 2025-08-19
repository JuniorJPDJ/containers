# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_22/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.33.1
# revision: 6
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.22.1@sha256:4bcff63911fcb4448bd4fdacec207030997caf25e9bea4045fa6c8c44de311d1

# renovate: datasource=repology depName=alpine_3_22/openssl versioning=loose
ARG   OPENSSL_VERSION="3.5.2-r0"
# renovate: datasource=repology depName=alpine_3_22/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.33.1-r1"
# renovate: datasource=repology depName=alpine_3_22/jq versioning=loose
ARG   JQ_VERSION="1.8.0-r0"
# renovate: datasource=repology depName=alpine_3_22/yq-go versioning=loose
ARG   YQ_VERSION="4.46.1-r1"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
      && \
      rm -rf /var/cache/apk/*
