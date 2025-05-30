# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_21/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.31.5
# revision: 6
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.22.0@sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715

# renovate: datasource=repology depName=alpine_3_21/openssl versioning=loose
ARG   OPENSSL_VERSION="3.3.3-r0"
# renovate: datasource=repology depName=alpine_3_21/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.31.5-r3"
# renovate: datasource=repology depName=alpine_3_21/jq versioning=loose
ARG   JQ_VERSION="1.7.1-r0"
# renovate: datasource=repology depName=alpine_3_21/yq-go versioning=loose
ARG   YQ_VERSION="4.44.5-r5"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
      && \
      rm -rf /var/cache/apk/*
