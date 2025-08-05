# platforms: linux/amd64,linux/arm64,linux/arm/v6
# renovate: datasource=docker depName=certbot/certbot extractVersion=^v(?<version>.*)$
# app_version: 4.2.0
# revision: 1
# description: Let's encrypt certbot with haproxy compatibility script and cron renew runner
FROM        certbot/certbot:v4.2.0@sha256:9626d72120577cf72da4fc7948806e9993598981720a4cbe04340a502468d67b


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
