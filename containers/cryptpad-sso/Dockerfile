# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad versioning=loose extractVersion=^version-(?<version>.*)$
# app_version: 2026.2.0
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2026.2.0@sha256:4ec173673d8d7f69fe04fa1f3f72d529c05d5ae2d70c5a38f59fcfcdd523fad1

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="0.5.1"

ADD   https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
