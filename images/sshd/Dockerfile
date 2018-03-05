FROM alpine:latest

WORKDIR /var/www/html/

# Install packages and create www-data user
RUN apk --no-cache update \
  && apk --no-cache add openssh-server \
    vim \
    shadow \
  && useradd -m -r -s /bin/sh -u 82 -U www-data \
  && echo www-data:www-data | chpasswd \
  && apk --no-cache del shadow \
  && rm -rf /var/cache/apk/* /tmp/*

# Configure SSH server
COPY etc/ssh/sshd_config /etc/ssh/sshd_config
RUN ssh-keygen -A

# Add SSH key to www-data user
COPY home/www-data /home/www-data
RUN ln -s /var/www/log/ /home/www-data/log \
  && ln -s /var/www/html/ /home/www-data/html \
  && chown -R www-data:www-data /home/www-data \
  && chmod 0644 /home/www-data/.ssh/authorized_keys

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
