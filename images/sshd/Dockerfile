FROM debian:stretch-slim

RUN mkdir -p /var/www/.ssh/
RUN mkdir -p /var/www/html/
RUN mkdir -p /var/www/log/
RUN mkdir -p /var/www/log/php/
RUN mkdir -p /var/www/log/nginx/

WORKDIR /var/www/html/

RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y openssh-server \
  tar \
  gzip \
  bzip2 \
  vim

# Add SSH key to www-data user
COPY var/www/.ssh/authorized_keys /var/www/.ssh/authorized_keys
RUN chmod 0644 /var/www/.ssh/authorized_keys
RUN chown www-data:www-data /var/www/.ssh/authorized_keys

# Allow www-data user to use SSH
RUN chsh -s /bin/bash www-data
RUN echo www-data:www-data | chpasswd

# Configure SSH server
COPY etc/ssh/sshd_config /etc/ssh/sshd_config
RUN mkdir /var/run/sshd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
