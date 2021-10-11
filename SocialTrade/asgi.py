"""
ASGI config for SocialTrade project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""


#ASGI is Asynchronous Gateway Interface which will be used by websocket
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialTrade.settings')

application = get_asgi_application()
