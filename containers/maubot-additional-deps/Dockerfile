# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=dock.mau.dev/maubot/maubot extractVersion=^v(?<version>.*)$
# app_version: 0.6.0
# revision: 1
# description: A plugin-based Matrix bot system with additional python libraries added.
FROM  dock.mau.dev/maubot/maubot:v0.6.0@sha256:6968ddea1e08aa7f8ac70ac7a706663fe8d7b4d6f96cd7a6bb8548637fb8cd17

RUN   pip3 install --break-system-packages \
        apscheduler \
        cron_descriptor
