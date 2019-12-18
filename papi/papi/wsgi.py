"""
WSGI config for papi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/server/python3.7/lib/python3.7/site-packages')
sys.path.append('/opt/server/python3.7/lib/python3.7/site-packages')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'papi.settings')

application = get_wsgi_application()
