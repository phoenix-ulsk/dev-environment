FROM nginx:mainline-alpine

ENV ROOT_PASSWORD=root

WORKDIR /var/www/html/

# Install additional dependencies and create www-data user
RUN apk --no-cache update && \
  apk --no-cache add openssl \
    shadow && \
  useradd -m -r -s /bin/sh -u 82 -U www-data && \
  echo www-data:www-data | chpasswd && \
  apk --no-cache del shadow && \
  rm -rf /var/cache/apk/* /tmp/*

# Create www volume structure, because we do not know what container is the first to run and seed data to volume.
# As a workaround for docker-compose v3 volumes management bug/feature: https://github.com/docker/compose/issues/4379
RUN mkdir -p /var/www/html/ && \
  mkdir -p /var/www/log/ && \
  mkdir -p /var/www/log/php/ && \
  mkdir -p /var/www/log/nginx/ && \
  chown www-data:www-data /var/www/html/ && \
  chown www-data:www-data /var/www/log/php/
COPY var/www/html/phpinfo.php /var/www/html/phpinfo.php

# Configure nginx
COPY etc/nginx /etc/nginx

# Create self signed certificate for HTTS
RUN mkdir /etc/ssl/self_signed/ && \
  openssl req \
    -x509 \
    -nodes \
    -days 1825 \
    -newkey rsa:2048 \
    -keyout /etc/ssl/self_signed/self_signed.key \
    -out /etc/ssl/self_signed/self_signed.crt \
    -subj "/C=GO/ST=Gondor/L=Minas Tirith/O=Heren Istarion"

EXPOSE 80 443
