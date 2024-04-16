# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.105.0
# revision: 1
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.105.0@sha256:cbd56af58232394066d3ab9e55316ac92ed4b8b9392a829812e333f5178be6c0

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
