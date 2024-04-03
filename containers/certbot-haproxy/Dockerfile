# platforms: linux/amd64,linux/arm64,linux/arm/v6
FROM        certbot/certbot:v2.10.0@sha256:8d785998c367a7c1058f9b8878fce4c728c725b4ba0fef57ed5322ef38b82613


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
