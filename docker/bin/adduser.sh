groupadd --system -g 80 www
adduser -r -o --home /www --uid 80 --gid 80 -s /sbin/nologin -c "Web Application" www
chown www:www -R /www