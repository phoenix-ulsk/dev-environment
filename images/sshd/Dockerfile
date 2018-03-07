FROM alpine:latest

WORKDIR /var/www/html/

# Install packages and create www-data user
RUN apk --no-cache update && \
  apk --no-cache add openssh-server \
    openssh-sftp-server \
    openssh-client \
    mysql-client \
    vim \
    git \
    git-bash-completion \
    shadow \
    bash \
    bash-doc \
    bash-completion \
    lftp \
    mc && \
  useradd -m -r -s /bin/bash -u 82 -U www-data && \
  echo www-data:www-data | chpasswd && \
  apk --no-cache del shadow && \
  rm -rf /var/cache/apk/* /tmp/* && \
  ssh-keygen -A

# Create www volume structure, because we do not know what container is the first to run and seed data to volume.
# As a workaround for docker-compose v3 volumes management bug/feature: https://github.com/docker/compose/issues/4379
RUN mkdir -p /var/www/html/ && \
  mkdir -p /var/www/log/ && \
  mkdir -p /var/www/log/php/ && \
  mkdir -p /var/www/log/nginx/ && \
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
  echo -e "alias mysqldump='mysqldump -hmysql5 -uroot -proot'" | tee -a /home/www-data/.profile > /dev/null
USER root

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
