# platforms: linux/amd64,linux/386,linux/arm64,linux/arm/v7,linux/ppc64le,linux/s390x
FROM  alpine:3.19.1@sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672bd4f27761f8e1ad6b

# renovate: datasource=repology depName=alpine_3_19/openssl versioning=loose
ARG   OPENSSL_VERSION="3.1.4-r5"
# renovate: datasource=repology depName=alpine_3_19/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.28.4-r1"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
      && \
      rm -rf /var/cache/apk/*
