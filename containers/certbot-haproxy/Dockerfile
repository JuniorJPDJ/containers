# platforms: linux/amd64,linux/arm64,linux/arm/v6
FROM        certbot/certbot:v2.9.0@sha256:953b5daac63b14e4f8b77aacf4831f916faac836c67cd12fcc6408201554962e


VOLUME      /etc/certs

COPY        crontab /etc/crontabs/root
COPY        cp_certs.sh /opt/
COPY        start.sh /opt/

ENTRYPOINT  ["/opt/start.sh"]
CMD         []
