"""
WSGI config for SocialTrade project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""


#WSGI is Website Gateway Interface which will be used by webserver
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialTrade.settings')

application = get_wsgi_application()
