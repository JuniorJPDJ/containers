# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.128.0
# revision: 2
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.128.0@sha256:5765b7f1bd46b3ded0a59546c8e69b33e57ef6007854791701943f0414557e39 AS builder

# renovate: datasource=github-tags depName=devture/matrix-synapse-shared-secret-auth
ARG   SHARED_SECRET_AUTH_VERSION="2.0.3"

ARG   DEBIAN_FRONTEND=noninteractive

RUN   apt update -y && \
      apt install -y git && \
      pip install --prefix="/install" --no-deps \
        git+https://github.com/devture/matrix-synapse-shared-secret-auth@${SHARED_SECRET_AUTH_VERSION}


FROM  ghcr.io/element-hq/synapse:v1.128.0@sha256:5765b7f1bd46b3ded0a59546c8e69b33e57ef6007854791701943f0414557e39

COPY --from=builder /install /usr/local
