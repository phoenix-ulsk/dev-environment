FROM alpine:edge

WORKDIR /var/www/html/

ARG GIT_USER_NAME
ARG GIT_USER_EMAIL
ARG GIT_EDITOR

# Install packages and create www-data user
RUN apk --no-cache update && \
  apk --no-cache add openssh-server \
    openssh-sftp-server \
    openssh-client \
    mysql-client \
    vim \
    git \
    git-bash-completion \
    git-diff-highlight \
    less \
    shadow \
    bash \
    bash-doc \
    bash-completion \
    lftp \
    mc \
    curl \
    php7 \
    php7-common \
    php7-calendar \
    php7-ctype \
    php7-curl \
    php7-dom \
    php7-fileinfo \
    php7-ftp \
    php7-gd \
    php7-iconv \
    php7-json \
    php7-mbstring \
    php7-mcrypt \
    php7-memcached \
    php7-mysqli \
    php7-mysqlnd \
    php7-openssl \
    php7-pdo \
    php7-pdo_mysql \
    php7-pdo_sqlite \
    php7-phar \
    php7-posix \
    php7-session \
    php7-simplexml \
    php7-soap \
    php7-sockets \
    php7-sqlite3 \
    php7-tokenizer \
    php7-xml \
    php7-xmlreader \
    php7-xmlwriter && \
  useradd -m -r -s /bin/bash -u 82 -U www-data && \
  echo www-data:www-data | chpasswd && \
  apk --no-cache del shadow && \
  rm -rf /var/cache/apk/* /tmp/* && \
  ssh-keygen -A

RUN curl -sS https://getcomposer.org/installer -o composer-setup.php && \
  php composer-setup.php --install-dir=/usr/local/bin --filename=composer && \
  rm composer-setup.php

# Create www volume structure, because we do not know what container is the first to run and seed data to volume.
# As a workaround for docker-compose v3 volumes management bug/feature: https://github.com/docker/compose/issues/4379
RUN mkdir -p /var/www/html/ && \
  mkdir -p /var/www/log/ && \
  mkdir -p /var/www/log/php/ && \
  mkdir -p /var/www/log/nginx/ && \
  mkdir -p /var/www/conf/ && \
  mkdir -p /var/www/conf/nginx/ && \
  chown www-data:www-data /var/www/html/ && \
  chown www-data:www-data /var/www/log/php/
COPY var/www/html/phpinfo.php /var/www/html/phpinfo.php

# Configure container
COPY etc/ssh/www-data.pub /etc/ssh/www-data.pub
RUN sed -i 's/AuthorizedKeysFile\t.ssh\/authorized_keys/AuthorizedKeysFile\t.ssh\/authorized_keys \/etc\/ssh\/www-data.pub/' /etc/ssh/sshd_config > /dev/null && \
  ln -s /var/www/log/ /home/www-data/log && \
  ln -s /var/www/html/ /home/www-data/html && \
  chown -R www-data:www-data /home/www-data

# Run user specific configs
USER www-data
RUN echo -e "#!/bin/bash" | tee -a /home/www-data/.profile > /dev/null && \
  echo -e "\nalias vi='vim'" | tee -a /home/www-data/.profile > /dev/null && \
  echo -e "\nalias mysql='mysql -hmysql5 -uroot -proot'" | tee -a /home/www-data/.profile > /dev/null && \
  echo -e "alias mysqldump='mysqldump -hmysql5 -uroot -proot'" | tee -a /home/www-data/.profile > /dev/null && \
  echo -e "[user]" | tee -a /home/www-data/.gitconfig > /dev/null && \
  echo -e "\tname = ${GIT_USER_NAME}" | tee -a /home/www-data/.gitconfig > /dev/null && \
  echo -e "\temail = ${GIT_USER_EMAIL}" | tee -a /home/www-data/.gitconfig > /dev/null && \
  echo -e "[core]" | tee -a /home/www-data/.gitconfig > /dev/null && \
  echo -e "\teditor = ${GIT_EDITOR}" | tee -a /home/www-data/.gitconfig > /dev/null

USER root

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
