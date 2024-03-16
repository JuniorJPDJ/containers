# platforms: linux/amd64,linux/arm64,linux/arm/v6
FROM        certbot/certbot:v2.9.0


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
