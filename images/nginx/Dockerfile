FROM nginx:latest

WORKDIR /var/www/html/

ADD etc/nginx/conf.d /etc/nginx/conf.d
COPY etc/nginx/fastcgi_params /etc/nginx/fastcgi_params
COPY etc/nginx/nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y \
  openssl

RUN mkdir /etc/ssl/self_signed/

RUN openssl req \
    -x509 \
    -nodes \
    -days 1825 \
    -newkey rsa:2048 \
    -keyout /etc/ssl/self_signed/self_signed.key \
    -out /etc/ssl/self_signed/self_signed.crt \
    -subj "/C=GO/ST=Gondor/L=Minas Tirith/O=Heren Istarion"

EXPOSE 80 443
