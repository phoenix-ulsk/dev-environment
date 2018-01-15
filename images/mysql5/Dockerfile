FROM mysql:5

ADD etc/mysql/mysql.conf.d /etc/mysql/mysql.conf.d

RUN mkdir /var/run/sock
RUN chown mysql:mysql /var/run/sock
RUN chmod 0777 /var/run/sock
