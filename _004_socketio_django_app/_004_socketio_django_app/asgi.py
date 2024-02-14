"""
ASGI config for _004_socketio_django_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from app.views import sio
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      '_004_socketio_django_app.settings')

django_application = get_asgi_application()

application = socketio.ASGIApp(sio, django_application)
