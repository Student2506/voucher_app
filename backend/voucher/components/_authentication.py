"""Authentication component."""

import os

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'django_auth_adfs.backend.AdfsAuthCodeBackend',
    'django_auth_adfs.backend.AdfsAccessTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]


AUTH_ADFS = {
    'SERVER': 'adfs.karo-film.ru',
    'CLIENT_ID': os.getenv('CLIENT_ID'),
    'RELYING_PARTY_ID': os.getenv('RELYING_PARTY_ID'),
    'AUDIENCE': os.getenv('AUDIENCE'),
    'CLAIM_MAPPING': {
        'first_name': 'given_name',
        'last_name': 'family_name',
        'email': 'email',
    },
    'USERNAME_CLAIM': 'winaccountname',
    'GROUP_CLAIM': 'group',
    'DISABLE_SSO': False,
    'LOGIN_EXEMPT_URLS': ['^admin', '^api'],
}
