FROM mysql:5

COPY etc/mysql/mysql.conf.d /etc/mysql/mysql.conf.d

RUN mkdir -p /var/run/sock \
  && chown mysql:mysql /var/run/sock \
  && chmod 0777 /var/run/sock
