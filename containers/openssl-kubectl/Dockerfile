# platforms: linux/amd64,linux/arm64,linux/arm/v7
# renovate: datasource=repology depName=alpine_3_24/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.36.1
# revision: 2
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.24.1@sha256:28bd5fe8b56d1bd048e5babf5b10710ebe0bae67db86916198a6eec434943f8b

# renovate: datasource=repology depName=alpine_3_24/openssl versioning=loose
ARG   OPENSSL_VERSION="3.5.7-r0"
# renovate: datasource=repology depName=alpine_3_24/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.36.1-r0"
# renovate: datasource=repology depName=alpine_3_24/jq versioning=loose
ARG   JQ_VERSION="1.8.1-r0"
# renovate: datasource=repology depName=alpine_3_24/yq-go versioning=loose
ARG   YQ_VERSION="4.53.3-r0"
# renovate: datasource=repology depName=alpine_3_24/bash versioning=loose
ARG   BASH_VERSION="5.3.9-r1"
# renovate: datasource=repology depName=alpine_3_24/prometheus versioning=loose
ARG   PROMETHEUS_VERSION="3.5.3-r1"
# renovate: datasource=repology depName=alpine_3_24/openssh versioning=loose
ARG   OPENSSH_VERSION="10.3_p1-r0"
# renovate: datasource=repology depName=alpine_3_24/coreutils versioning=loose
ARG   COREUTILS_VERSION="9.11-r0"

RUN   apk add --no-cache \
        openssl=${OPENSSL_VERSION} \
        kubectl=${KUBECTL_VERSION} \
        jq=${JQ_VERSION} \
        yq-go=${YQ_VERSION} \
        bash=${BASH_VERSION} \
        prometheus=${PROMETHEUS_VERSION} \
        openssh-client=${OPENSSH_VERSION} \
        coreutils=${COREUTILS_VERSION} \
      && \
      rm -rf /var/cache/apk/* && \
      rm /usr/bin/prometheus    # unneccessary 130MB, we want just promtool
