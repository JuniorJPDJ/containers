# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad extractVersion=^version-(?<version>.*)$
# app_version: 2025.9.0
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2025.9.0@sha256:353d98ac893158b699dcf345b6c8271dea9200d1015a9d367441625c046486e4

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="0.5.0"

ADD   https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
