"""Django settings for voucher project."""

import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1').split(',')
include('components/_apps_mid.py')
ROOT_URLCONF = 'voucher.urls'
include('components/_templates.py')
WSGI_APPLICATION = 'voucher.wsgi.application'
include('components/_database.py')
include('components/_locale.py')
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'django_auth_adfs.rest_framework.AdfsAccessTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'voucher_api.paginators.StandardResultsSetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    'PAGE_SIZE': os.getenv('PAGE_SIZE', 10),
}
include('components/_authentication.py')

LOGIN_REDIRECT_URL = 'retrieve-token'
LOGIN_URL = 'django_auth_adfs:login'
CORS_ALLOW_ALL_ORIGINS = True
