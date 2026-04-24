# platforms: linux/amd64,linux/arm64,linux/arm/v7
# renovate: datasource=repology depName=alpine_3_23/kubectl versioning=loose extractVersion=^(?<version>.*)-r\d+$
# app_version: 1.34.2
# revision: 12
# description: Small image with kubectl and openssl designed as a helper for kubernetes hook jobs
FROM  alpine:3.23.4@sha256:5b10f432ef3da1b8d4c7eb6c487f2f5a8f096bc91145e68878dd4a5019afde11

# renovate: datasource=repology depName=alpine_3_23/openssl versioning=loose
ARG   OPENSSL_VERSION="3.5.6-r0"
# renovate: datasource=repology depName=alpine_3_23/kubectl versioning=loose
ARG   KUBECTL_VERSION="1.34.2-r5"
# renovate: datasource=repology depName=alpine_3_23/jq versioning=loose
ARG   JQ_VERSION="1.8.1-r0"
# renovate: datasource=repology depName=alpine_3_23/yq-go versioning=loose
ARG   YQ_VERSION="4.49.2-r5"
# renovate: datasource=repology depName=alpine_3_23/bash versioning=loose
ARG   BASH_VERSION="5.3.3-r1"
# renovate: datasource=repology depName=alpine_3_23/prometheus versioning=loose
ARG   PROMETHEUS_VERSION="3.5.0-r7"
# renovate: datasource=repology depName=alpine_3_23/openssh versioning=loose
ARG   OPENSSH_VERSION="10.2_p1-r0"
# renovate: datasource=repology depName=alpine_3_23/coreutils versioning=loose
ARG   COREUTILS_VERSION="9.8-r1"

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
      rm /usr/bin/prometheus    # unneccessary 130MB
