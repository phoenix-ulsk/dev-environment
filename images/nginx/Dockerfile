FROM nginx:mainline-alpine

ENV ROOT_PASSWORD=root

WORKDIR /var/www/html/

RUN mkdir -p /var/www/html/ \
  && mkdir -p /var/www/log/ \
  && mkdir -p /var/www/log/php/ \
  && mkdir -p /var/www/log/nginx/

# Install additional dependencies
RUN apk --no-cache update \
  && apk --no-cache add openssl \
  && rm -rf /var/cache/apk/* /tmp/*

# Configure nginx
COPY etc/nginx /etc/nginx

# Config local hosts file
RUN echo -e "# Local webserver hosts" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev56.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev71.local" | tee -a /etc/hosts > /dev/null

# Create self signed certificate for HTTS
RUN mkdir /etc/ssl/self_signed/ \
  && openssl req \
    -x509 \
    -nodes \
    -days 1825 \
    -newkey rsa:2048 \
    -keyout /etc/ssl/self_signed/self_signed.key \
    -out /etc/ssl/self_signed/self_signed.crt \
    -subj "/C=GO/ST=Gondor/L=Minas Tirith/O=Heren Istarion"

EXPOSE 80 443
