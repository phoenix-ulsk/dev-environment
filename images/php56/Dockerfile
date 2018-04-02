FROM php:5.6-fpm-alpine

ENV ROOT_PASSWORD=root

WORKDIR /var/www/html/

# Install aditional libs
RUN apk --no-cache update && \
  apk --no-cache add mysql-client \
    ssmtp \
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
    ${PHPIZE_DEPS} && \
  pecl install memcached-2.2.0 xdebug-2.5.5 && \
  docker-php-ext-configure gd \
    --with-freetype-dir=/usr/include/ \
    --with-png-dir=/usr/include/ \
    --with-jpeg-dir=/usr/include/ && \
  NPROC=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1) && \
  docker-php-ext-install -j${NPROC} gd \
    pdo_mysql && \
  docker-php-ext-enable memcached \
    xdebug \
    opcache && \
  apk --no-cache del freetype-dev \
    libpng-dev \
    libjpeg-turbo-dev \
    libmemcached-dev \
    cyrus-sasl-dev \
    pcre-dev \
    ${PHPIZE_DEPS} && \
  rm -rf /var/cache/apk/* /tmp/* && \
  curl -sS https://getcomposer.org/installer -o composer-setup.php && \
  php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
  rm composer-setup.php

# Create www volume structure, because we do not know what container is the first to run and seed data to volume.
# As a workaround for docker-compose v3 volumes management bug/feature: https://github.com/docker/compose/issues/4379
RUN mkdir -p /var/www/html/ && \
  mkdir -p /var/www/log/ && \
  mkdir -p /var/www/log/php/ && \
  mkdir -p /var/www/log/nginx/ && \
  chown www-data:www-data /var/www/html/ && \
  chown www-data:www-data /var/www/log/php/
COPY var/www/html/phpinfo.php /var/www/html/phpinfo.php

# Configure SSMTP and PHP
COPY usr/local/etc/php/php.ini /usr/local/etc/php/php.ini
RUN sed -i 's/mailhub=mail/mailhub=mailcatcher:1025/' /etc/ssmtp/ssmtp.conf > /dev/null && \
  sed -i 's/#hostname="localhost"/hostname=dev.local/' /etc/ssmtp/ssmtp.conf > /dev/null && \
  echo -e "FromLineOverride=YES" | tee -a /etc/ssmtp/ssmtp.conf > /dev/null && \
  sed -i 's/;error_log = log\/php-fpm.log/error_log = \/var\/www\/log\/php\/56-fpm.log/' /usr/local/etc/php-fpm.conf > /dev/null && \
  sed -i 's/;slowlog = log\/\$pool.log.slow/slowlog = \/var\/www\/log\/php\/56-slow.log/' /usr/local/etc/php-fpm.d/www.conf > /dev/null && \
  sed -i 's/;request_slowlog_timeout = 0/request_slowlog_timeout = 3/' /usr/local/etc/php-fpm.d/www.conf > /dev/null && \
  sed -i 's/pm = dynamic/pm = static/' /usr/local/etc/php-fpm.d/www.conf > /dev/null && \
  sed -i 's/pm.max_children = 5/pm.max_children = 2/' /usr/local/etc/php-fpm.d/www.conf > /dev/null && \
  sed -i 's/;pm.max_requests = 500/pm.max_requests = 1000/' /usr/local/etc/php-fpm.d/www.conf > /dev/null && \
  echo -e "opcache.enable=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.use_cwd=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.revalidate_path=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.validate_timestamps=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.revalidate_freq=0" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.save_comments=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.load_comments=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.max_accelerated_files=10000" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.memory_consumption=64" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.interned_strings_buffer=16" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "opcache.fast_shutdown=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-opcache.ini > /dev/null && \
  echo -e "xdebug.remote_enable=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_autostart=0" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_connect_back=0" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_handler=dbgp" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_mode=req" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_host=10.254.254.254" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.remote_port=9056" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.profiler_enable=0" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.profiler_enable_trigger=1" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.max_nesting_level=500" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null && \
  echo -e "xdebug.idekey=PHPSTORM" | tee -a /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini > /dev/null

USER www-data

EXPOSE 9000 9056
