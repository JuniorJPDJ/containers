# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=dock.mau.dev/maubot/maubot extractVersion=^v(?<version>.*)$
# app_version: 0.5.2
# revision: 1
# description: A plugin-based Matrix bot system with additional python libraries added.
FROM  dock.mau.dev/maubot/maubot:v0.5.2@sha256:b9f28d08d926a8522da1b220374e7fd50b32b07311c21fc6ca6f0690f9fb5402

RUN   pip3 install --break-system-packages \
        apscheduler \
        cron_descriptor
