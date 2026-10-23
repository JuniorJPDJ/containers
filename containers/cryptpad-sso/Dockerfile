# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad versioning=loose extractVersion=^version-(?<version>.*)$
# app_version: 2026.10.0
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2026.10.0@sha256:61a12565a532a046996e47b3180a8ac9855d86c262dc98a1bb8d1107557bfe3a

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="0.6.0"

ADD   https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
