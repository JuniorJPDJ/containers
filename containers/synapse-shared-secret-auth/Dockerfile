# platforms: linux/amd64,linux/arm64
FROM  ghcr.io/element-hq/synapse:v1.102.0@sha256:6c1ae2e6d04de4545e9e006b678cb2f8bf2880e5c476d453ea3ca08a3d9472d6

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
