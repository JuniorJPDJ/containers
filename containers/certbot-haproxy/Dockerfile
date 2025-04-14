# platforms: linux/amd64,linux/arm64,linux/arm/v6
# renovate: datasource=docker depName=certbot/certbot extractVersion=^v(?<version>.*)$
# app_version: 4.0.0
# revision: 1
# description: Let's encrypt certbot with haproxy compatibility script and cron renew runner
FROM        certbot/certbot:v4.0.0@sha256:0e40d51116b9e1058466aa2fd8f342b1d676dfbc17e47877a9e02c3e2460580a


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
