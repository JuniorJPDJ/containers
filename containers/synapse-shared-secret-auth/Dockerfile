# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=ghcr.io/element-hq/synapse extractVersion=^v(?<version>.*)$
# app_version: 1.142.0
# revision: 1
# description: Matrix Synapse homeserver with matrix-synapse-shared-secret-auth preinstalled
FROM  ghcr.io/element-hq/synapse:v1.142.0@sha256:f33543130e015d85c27a6d736e2ae013a845954203f4b0163c5f170123f2b3b1 AS builder

# renovate: datasource=github-tags depName=devture/matrix-synapse-shared-secret-auth
ARG   SHARED_SECRET_AUTH_VERSION="2.0.3"

ARG   DEBIAN_FRONTEND=noninteractive

RUN   apt update -y && \
      apt install -y git && \
      pip install --prefix="/install" --no-deps \
        git+https://github.com/devture/matrix-synapse-shared-secret-auth@${SHARED_SECRET_AUTH_VERSION}


FROM  ghcr.io/element-hq/synapse:v1.142.0@sha256:f33543130e015d85c27a6d736e2ae013a845954203f4b0163c5f170123f2b3b1

COPY --from=builder /install /usr/local
