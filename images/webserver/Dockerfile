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

# Install PHP 5.6
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

# Install PHP 7.0
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

# Install PHP 7.1
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

# Install PHP 7.2
RUN apt-get install -y \
  php7.2 \
  php7.2-cli \
  php7.2-common \
  php7.2-curl \
  php7.2-dev \
  php7.2-fpm \
  php7.2-gd \
  php7.2-mbstring \
  php7.2-mysql \
  php7.2-opcache \
  php7.2-xsl

# Install PHP libs
RUN apt-get install -y \
  php-pear \
  php-twig \
  php-xdebug \
  php-memcached

COPY etc/php/5.6 /etc/php/5.6
COPY etc/php/7.0 /etc/php/7.0
COPY etc/php/7.1 /etc/php/7.1
COPY etc/php/7.2 /etc/php/7.2
COPY etc/nginx /etc/nginx

# Add nginx to www-data grout
RUN adduser nginx www-data
RUN chown www-data:www-data /var/www/*

# Install composer
RUN curl -sS https://getcomposer.org/installer -o composer-setup.php \
  && php composer-setup.php --install-dir=/usr/local/bin --filename=composer \
  && rm composer-setup.php

# Config local hosts file
RUN echo -e "# Local webserver hosts" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev5.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev70.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev71.local" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev72.local" | tee -a /etc/hosts > /dev/null

RUN mkdir /etc/ssl/self_signed/ \
  && openssl req \
    -x509 \
    -nodes \
    -days 1825 \
    -newkey rsa:2048 \
    -keyout /etc/ssl/self_signed/self_signed.key \
    -out /etc/ssl/self_signed/self_signed.crt \
    -subj "/C=GO/ST=Gondor/L=Minas Tirith/O=Heren Istarion"

# Copy wrapper script to run all php-fpm daemons
COPY root/wrapper_script.sh /root/wrapper_script.sh
RUN chmod 0755 /root/wrapper_script.sh

EXPOSE 80 443

CMD /root/wrapper_script.sh
