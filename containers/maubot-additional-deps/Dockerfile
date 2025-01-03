# platforms: linux/amd64,linux/arm64
# renovate: datasource=docker depName=dock.mau.dev/maubot/maubot extractVersion=^v(?<version>.*)$
# app_version: 0.5.1
# revision: 1
# description: A plugin-based Matrix bot system with additional python libraries added.
FROM  dock.mau.dev/maubot/maubot:v0.5.1@sha256:65bbb08f1eb294cd470ecc5cf88403f4dc9bcd13f905753fbb254c616bfa03e7

RUN   pip3 install --break-system-packages \
        apscheduler \
        cron_descriptor
