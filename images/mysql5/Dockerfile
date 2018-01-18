FROM mysql:5

ADD etc/mysql/mysql.conf.d /etc/mysql/mysql.conf.d

RUN mkdir -p /var/run/sock \
  && chown mysql:mysql /var/run/sock \
  && chmod 0777 /var/run/sock

RUN mkdir -p /var/www/log/mysql5 \
  && chown mysql:mysql /var/www/log/mysql5 \
  && chmod 0777 /var/www/log/mysql5
