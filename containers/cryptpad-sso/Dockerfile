# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad versioning=loose extractVersion=^version-(?<version>.*)$
# app_version: 2026.2.2
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2026.2.2@sha256:34bb676e358ce6609602aad8a7362b435f2bb349221057c0160c94a0aa54bcc7

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="0.5.1"

ADD   https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
