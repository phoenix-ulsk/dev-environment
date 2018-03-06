FROM alpine:latest

WORKDIR /var/www/html/

# Install packages and create www-data user
RUN apk --no-cache update \
  && apk --no-cache add openssh-server \
    openssh-sftp-server \
    vim \
    git \
    git-bash-completion \
    shadow \
  && useradd -m -r -s /bin/sh -u 82 -U www-data \
  && echo www-data:www-data | chpasswd \
  && apk --no-cache del shadow \
  && rm -rf /var/cache/apk/* /tmp/* \
  && ssh-keygen -A

# Create www volume structure (because we do not know what container is the first to run)
RUN mkdir -p /var/www/html/ \
  && mkdir -p /var/www/log/ \
  && mkdir -p /var/www/log/php/ \
  && mkdir -p /var/www/log/nginx/ \
  && chown www-data:www-data /var/www/html/ \
  && chown www-data:www-data /var/www/log/php/
COPY var/www/html/phpinfo.php /var/www/html/phpinfo.php

# Add SSH key to www-data user
COPY home/www-data /home/www-data
RUN ln -s /var/www/log/ /home/www-data/log \
  && ln -s /var/www/html/ /home/www-data/html \
  && chown -R www-data:www-data /home/www-data \
  && chmod 0644 /home/www-data/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
