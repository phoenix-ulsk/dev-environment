#!/bin/bash

# Start php 5.6 fpm daemon
php-fpm5.6 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start  php fpm 5.6: $status"
  exit $status
fi

# Start php 7.0 fpm daemon
php-fpm7.0 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start php fpm 7.0: $status"
  exit $status
fi

# Start php 7.1 fpm daemon
php-fpm7.1 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start php fpm 7.1: $status"
  exit $status
fi

# Start php 7.2 fpm daemon
php-fpm7.2 -D
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start php fpm 7.2: $status"
  exit $status
fi

# Start nginx
nginx -g 'daemon off;'
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start nginx: $status"
  exit $status
fi

# Naive check runs checks once a minute to see if either of the processes exited.
# This illustrates part of the heavy lifting you need to do if you want to run
# more than one service in a container. The container exits with an error
# if it detects that either of the processes has exited.
# Otherwise it loops forever, waking up every 60 seconds

while sleep 60; do
  ps aux | grep php/5.6 | grep -q -v grep
  PHP56_STATUS=$?
  ps aux | grep php/7.0 | grep -q -v grep
  PHP70_STATUS=$?
  ps aux | grep php/7.1 | grep -q -v grep
  PHP71_STATUS=$?
  ps aux | grep php/7.2 | grep -q -v grep
  PHP72_STATUS=$?
  ps aux | grep nginx | grep -q -v grep
  NGINX_STATUS=$?
  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ $PHP56_STATUS -ne 0 -o $PHP70_STATUS -ne 0 -o $PHP71_STATUS -ne 0 -o $PHP72_STATUS -ne 0 -o $NGINX_STATUS -ne 0 ]; then
    echo "One of the processes has already exited."
    exit -1
  fi
done
