# platforms: linux/amd64,linux/arm64,linux/arm/v6
# renovate: datasource=docker depName=certbot/certbot extractVersion=^v(?<version>.*)$
# app_version: 5.1.0
# revision: 1
# description: Let's encrypt certbot with haproxy compatibility script and cron renew runner
FROM        certbot/certbot:v5.1.0@sha256:bb72eb98a32ecc5dcef8eeeb8fb6a2a8c50d4d93e2a2c3542f8cb679840c990c


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
