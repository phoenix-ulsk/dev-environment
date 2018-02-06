FROM nginx:latest

WORKDIR /var/www/html/

RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y apt-transport-https \
  ca-certificates \
  curl \
  gnupg2 \
  software-properties-common \
  git \
  mysql-client \
  zip \
  ssmtp \
  openssl

RUN curl -fsSL https://packages.sury.org/php/apt.gpg | apt-key add - \
  && echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list \
  && apt-get update

RUN apt-get install -y \
  php5.6 \
  php5.6-cli \
  php5.6-common \
  php5.6-curl \
  php5.6-dev \
  php5.6-fpm \
  php5.6-gd \
  php5.6-mbstring \
  php5.6-mcrypt \
  php5.6-mysql \
  php5.6-opcache \
  php5.6-xsl

RUN apt-get install -y \
  php7.0 \
  php7.0-cli \
  php7.0-common \
  php7.0-curl \
  php7.0-dev \
  php7.0-fpm \
  php7.0-gd \
  php7.0-mbstring \
  php7.0-mcrypt \
  php7.0-mysql \
  php7.0-opcache \
  php7.0-xsl

RUN apt-get install -y \
  php7.1 \
  php7.1-cli \
  php7.1-common \
  php7.1-curl \
  php7.1-dev \
  php7.1-fpm \
  php7.1-gd \
  php7.1-mbstring \
  php7.1-mcrypt \
  php7.1-mysql \
  php7.1-opcache \
  php7.1-xsl

RUN apt-get install -y \
  php-pear \
  php-twig \
  php-xdebug \
  php-memcached

COPY etc/php/5.6 /etc/php/5.6
COPY etc/php/7.0 /etc/php/7.0
COPY etc/php/7.1 /etc/php/7.1
COPY etc/nginx /etc/nginx

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
