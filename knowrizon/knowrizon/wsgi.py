"""
WSGI config for knowrizon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from knowrizon.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowrizon.settings')

application = get_wsgi_application()
# wsgi.py
from whitenoise import WhiteNoise

application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
