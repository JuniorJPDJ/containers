# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
# renovate: datasource=repology depName=alpine_3_20/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.30.0
# revision: 13
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.20.3@sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd1367effd16dc0d06d

# renovate: datasource=repology depName=alpine_3_20/openssl versioning=loose
ARG   OPENSSL_VERSION="3.3.2-r0"
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
