# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_21/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.31.5
# revision: 5
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.21.3@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c

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
