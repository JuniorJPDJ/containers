# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_20/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.30.0
# revision: 5
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.20.0@sha256:77726ef6b57ddf65bb551896826ec38bc3e53f75cdde31354fbffb4f25238ebd

# renovate: datasource=repology depName=alpine_3_20/openssl versioning=loose
ARG   OPENSSL_VERSION="3.3.1-r0"
# renovate: datasource=repology depName=alpine_3_20/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.30.0-r2"
# renovate: datasource=repology depName=alpine_3_20/jq versioning=loose
ARG   JQ_VERSION="1.7.1-r0"
# renovate: datasource=repology depName=alpine_3_20/yq-go versioning=loose
ARG   YQ_VERSION="4.44.1-r1"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
      && \
      rm -rf /var/cache/apk/*
