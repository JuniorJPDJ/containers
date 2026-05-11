# platforms: linux/amd64,linux/arm64,linux/arm/v6
# renovate: datasource=docker depName=certbot/certbot extractVersion=^v(?<version>.*)$
# app_version: 5.6.0
# revision: 1
# description: Let's encrypt certbot with haproxy compatibility script and cron renew runner
FROM        certbot/certbot:v5.6.0@sha256:0107d084c225631fc64a8313e19adb07275f7296fde338f7dfa93986c80b2e3e


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
