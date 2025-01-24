"""
ASGI config for knowrizon project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from knowrizon.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'knowrizon.settings')

application = get_asgi_application()
# wsgi.py
from whitenoise import WhiteNoise

application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
