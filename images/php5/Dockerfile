FROM debian:jessie-slim

WORKDIR /var/www/html/

RUN apt-get update && apt-get install -y \
  php5 \
  php5-common \
  php5-cli \
  php5-cgi \
  php5-mysql \
  php5-dev \
  php5-gd \
  php5-curl \
  php5-xsl \
  php5-memcached \
  php5-mcrypt \
  php5-fpm \
  php5-twig \
  php5-xdebug \
  php-pear \
  curl \
  git

RUN php5dismod mysqli

COPY etc/php5/mods-available/xdebug.ini /etc/php5/mods-available/xdebug.ini
COPY etc/php5/mods-available/opcache.ini /etc/php5/mods-available/opcache.ini

RUN php -r "copy('https://getcomposer.org/installer', '/tmp/composer-setup.php');" && \
  php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
  rm /tmp/composer-setup.php

# Change to fpm process later
CMD ["php5-fpm", "-F"]
