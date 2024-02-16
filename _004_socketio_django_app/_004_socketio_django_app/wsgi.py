"""
WSGI config for _004_socketio_django_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from app.sockets import sio
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '_004_socketio_django_app.settings')

django_application = get_wsgi_application()
application = socketio.WSGIApp(sio, django_application)
