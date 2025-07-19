#!/usr/bin/env bash
set -eu

# prepare static files

python manage.py collectstatic --no-input

# start the web server

nginx

# start the application server

python -m gunicorn -c $GUNICORN_CONF pems_web.wsgi
