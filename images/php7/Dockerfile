FROM debian:stretch-slim

WORKDIR /var/www/html/

RUN apt-get update && apt-get install -y \
  php7.0 \
  php7.0-common \
  php7.0-cli \
  php7.0-cgi \
  php7.0-mysql \
  php7.0-dev \
  php7.0-gd \
  php7.0-curl \
  php7.0-xsl \
  php7.0-memcached \
  php7.0-mcrypt \
  php7.0-fpm \
  php7.0-xdebug \
  php7.0-mbstring \
  php-pear \
  curl \
  git \
  mysql-client \
  zip \
  ssmtp

RUN phpdismod mysqli

ADD etc/php/7.0/fpm/pool.d /etc/php/7.0/fpm/pool.d
COPY etc/php/7.0/cli/php.ini /etc/php/7.0/cli/php.ini
COPY etc/php/7.0/fpm/php.ini /etc/php/7.0/fpm/php.ini
COPY etc/php/7.0/fpm/php-fpm.conf /etc/php/7.0/fpm/php-fpm.conf
COPY etc/php/7.0/mods-available/xdebug.ini /etc/php/7.0/mods-available/xdebug.ini
COPY etc/php/7.0/mods-available/opcache.ini /etc/php/7.0/mods-available/opcache.ini
COPY etc/ssmtp/ssmtp.conf /etc/ssmtp/ssmtp.conf

RUN php -r "copy('https://getcomposer.org/installer', '/tmp/composer-setup.php');" && \
  php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
  rm /tmp/composer-setup.php

EXPOSE 9002

# Change to fpm process later
CMD ["php-fpm7.0", "-F"]
