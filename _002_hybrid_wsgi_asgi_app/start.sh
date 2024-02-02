#!/usr/bin/env bash
SERVER=WSGI uwsgi --ini uwsgi.ini &
SERVER=ASGI python manage.py runserver 127.0.0.1:8001 &
