# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.124.0
# revision: 1
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.124.0@sha256:31f08252df11421dcbbbcff8333874b99b911a146508f14c6ac758ce9b9ce634

# renovate: datasource=github-tags depName=devture/matrix-synapse-shared-secret-auth
ARG   SHARED_SECRET_AUTH_VERSION="2.0.3"

ARG   DEBIAN_FRONTEND=noninteractive

RUN   apt update -y && \
      apt install -y git && \
      pip install --no-cache-dir \
        git+https://github.com/devture/matrix-synapse-shared-secret-auth@${SHARED_SECRET_AUTH_VERSION} \
      && \
      apt purge -y git && \
      apt autoremove -y && \
      rm -rf /var/lib/apt/lists/*
