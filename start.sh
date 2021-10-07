#!/bin/bash

# python manage.py migrate
# python manage.py collectstatic --no-input

mkdir -p /webapp/logs/
touch /webapp/logs/gunicorn.log
touch /webapp/logs/access.log
touch /webapp/logs/error.log
tail -n 0 -f /webapp/logs/*.log &

NAME='webapp'
NUM_WORKERS=3
DJANGO_WSGI_MODULE=aagesuite.wsgi
LOGFILE=/webapp/logs/gunicorn.log
ACCESS_LOGFILE=/webapp/logs/access.log
ERROR_LOGFILE=/webapp/logs/error.log

echo 'Starting $NAME as `whoami`'

exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind 0.0.0.0:8000 \
  --log-level=info \
  --log-file=$LOGFILE \
  --access-logfile=$ACCESS_LOGFILE \
  --error-logfile=$ERROR_LOGFILE \
