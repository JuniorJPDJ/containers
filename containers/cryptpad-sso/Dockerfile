# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad versioning=loose extractVersion=^version-(?<version>.*)$
# app_version: 2026.5.0
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2026.5.0@sha256:d605f55243aa9dc2851393c06ed44ace25f61cd7f3236de25dfa4aba1cc886b4

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="0.5.1"

ADD   https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
