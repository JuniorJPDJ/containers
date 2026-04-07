# platforms: linux/amd64,linux/arm64,linux/arm/v6
# renovate: datasource=docker depName=certbot/certbot extractVersion=^v(?<version>.*)$
# app_version: 5.5.0
# revision: 1
# description: Let's encrypt certbot with haproxy compatibility script and cron renew runner
FROM        certbot/certbot:v5.5.0@sha256:78a7eaa40af657301e25731297b6e73646c695370d17e9bb03189fa82966d65c


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
