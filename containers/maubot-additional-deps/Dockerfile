# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=dock.mau.dev/maubot/maubot extractVersion=^v(?<version>.*)$
# app_version: 0.5.0
# revision: 1
# description: A plugin-based Matrix bot system with additional python libraries added.
FROM  dock.mau.dev/maubot/maubot:v0.5.0@sha256:9842a0f385ede2000800a1733a32029b579e6dbf0dd60989cffa433429bcf79b

RUN   pip3 install --break-system-packages \
        apscheduler \
        cron_descriptor
