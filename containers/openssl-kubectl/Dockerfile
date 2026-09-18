# platforms: linux/amd64,linux/arm64,linux/arm/v7
# renovate: datasource=repology depName=alpine_3_24/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.36.1
# revision: 4
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.24.2@sha256:294b683cb724975bec92580e1e685676bd4b50bda910ddb8c51d4cabeaec77e6

# renovate: datasource=repology depName=alpine_3_24/openssl versioning=loose
ARG   OPENSSL_VERSION="3.5.8-r0"
# renovate: datasource=repology depName=alpine_3_24/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.36.1-r1"
# renovate: datasource=repology depName=alpine_3_24/jq versioning=loose
ARG   JQ_VERSION="1.8.2-r0"
# renovate: datasource=repology depName=alpine_3_24/yq-go versioning=loose
ARG   YQ_VERSION="4.53.3-r1"
# renovate: datasource=repology depName=alpine_3_24/bash versioning=loose
ARG   BASH_VERSION="5.3.9-r1"
# renovate: datasource=repology depName=alpine_3_24/prometheus versioning=loose
ARG   PROMETHEUS_VERSION="3.5.3-r2"
# renovate: datasource=repology depName=alpine_3_24/openssh versioning=loose
ARG   OPENSSH_VERSION="10.3_p1-r1"
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
