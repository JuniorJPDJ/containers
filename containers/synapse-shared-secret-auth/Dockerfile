# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.125.0
# revision: 1
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.125.0@sha256:b4d45c5158281ca5b97b4cf1154e16084ffcc9173716a33c5dab54a9798ecf23

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
