# platforms: linux/amd64,linux/arm64
FROM  ghcr.io/element-hq/synapse:v1.102.0

ARG   DEBIAN_FRONTEND=noninteractive

RUN   apt update -y && \
      apt install -y git && \
      pip install --no-cache-dir git+https://github.com/devture/matrix-synapse-shared-secret-auth && \
      apt purge -y git && \
      apt autoremove -y && \
      rm -rf /var/lib/apt/lists/*
