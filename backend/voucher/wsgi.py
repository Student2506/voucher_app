"""WSGI config for voucher project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'voucher.settings')

application = get_wsgi_application()
