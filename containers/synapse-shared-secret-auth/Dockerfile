# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.147.1
# revision: 1
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.147.1@sha256:c545d9e2b6fc36457757a932853d8fd3b2a7eee72cc5c192c691b324953f2623 AS builder

# renovate: datasource=github-tags depName=devture/matrix-synapse-shared-secret-auth
ARG   SHARED_SECRET_AUTH_VERSION="2.0.3"

ARG   DEBIAN_FRONTEND=noninteractive

RUN   apt update -y && \
      apt install -y git && \
      pip install --prefix="/install" --no-deps \
        git+https://github.com/devture/matrix-synapse-shared-secret-auth@${SHARED_SECRET_AUTH_VERSION}


FROM  ghcr.io/element-hq/synapse:v1.147.1@sha256:c545d9e2b6fc36457757a932853d8fd3b2a7eee72cc5c192c691b324953f2623

COPY --from=builder /install /usr/local
