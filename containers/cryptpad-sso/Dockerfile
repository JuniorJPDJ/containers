# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=cryptpad/cryptpad versioning=loose extractVersion=^version-(?<version>.*)$
# app_version: 2026.10.1
# revision: 1
# description: CryptPad with SSO plugin preinstalled
FROM  cryptpad/cryptpad:version-2026.10.1@sha256:b1129d954692e9b8a7d198e79d3080d3627051c95137bbf41a7d2683aa53305d

# renovate: datasource=github-tags depName=cryptpad/sso
ARG   CRYPTPAD_SSO_PLUGIN_VERSION="1.0.0"

ADD   --chown=cryptpad:cryptpad \
      https://github.com/cryptpad/sso.git#${CRYPTPAD_SSO_PLUGIN_VERSION} lib/plugins/sso
RUN   cd lib/plugins/sso && \
      npm ci --omit=dev && \
      rm -rf /cryptpad/.npm
