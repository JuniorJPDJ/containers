# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=dock.mau.dev/maubot/maubot extractVersion=^v(?<version>.*)$
# app_version: 0.6.1
# revision: 1
# description: A plugin-based Matrix bot system with additional python libraries added.
FROM  dock.mau.dev/maubot/maubot:v0.6.1@sha256:a0d77af42a4ccafc369e7ba086caa871acaa5909fdcff88a65b4c9f9e90ebacd

RUN   pip3 install --break-system-packages \
        apscheduler \
        cron_descriptor
