FROM php:5.6-fpm-alpine

ENV ROOT_PASSWORD=root

WORKDIR /var/www/html/

# Install aditional libs
RUN apk --no-cache update
RUN apk --no-cache add ssmtp \
    freetype \
    libpng \
    libjpeg-turbo \
    libmemcached \
    cyrus-sasl \
    freetype-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    libmemcached-dev \
    cyrus-sasl-dev \
    pcre-dev \
    ${PHPIZE_DEPS} \
  && pecl install memcached-2.2.0 xdebug-2.5.5 \
  && docker-php-ext-configure gd \
    --with-freetype-dir=/usr/include/ \
    --with-png-dir=/usr/include/ \
    --with-jpeg-dir=/usr/include/ \
  && NPROC=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1) \
  && docker-php-ext-install -j${NPROC} gd \
    pdo_mysql \
  && docker-php-ext-enable memcached \
    xdebug \
    opcache \
  && apk --no-cache del freetype-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    libmemcached-dev \
    cyrus-sasl-dev \
    pcre-dev \
    ${PHPIZE_DEPS} \
  && rm -rf /var/cache/apk/* /tmp/*

# Config local hosts file
RUN echo -e "# Local webserver hosts" | tee -a /etc/hosts > /dev/null \
  && echo -e "127.0.0.1\tdev56.local" | tee -a /etc/hosts > /dev/null
