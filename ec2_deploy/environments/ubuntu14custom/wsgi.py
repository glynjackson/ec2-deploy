import os
import sys
"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

path = '/srv/DOMAIN'
if path not in sys.path:
    sys.path.insert(0, '/srv/DOMAIN')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DOMAIN.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
