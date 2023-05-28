LOG_FORMAT = (
    '%(asctime)s [%(levelname)s] [%(request_id)s - %(username)s] %(name) -30s %(funcName) -35s %(lineno) -5d:'
    '%(message)s'
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'request_id': {
            '()': 'voucher_app.logging.RequestIdFilter',
        },
    },
    'formatters': {
        'default': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'debug-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'filters': ['require_debug_true', 'request_id'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['debug-console'],
            'propagate': False,
            'filters': ['request_id'],
        },
        'django': {
            'level': 'DEBUG',
            'handlers': ['debug-console'],
            'propagate': True,
            'filters': ['request_id'],
        },
        'django.request': {
            'handlers': ['debug-console'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['request_id'],
        },
        'voucher_app': {
            'handlers': ['debug-console'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['request_id'],
        },
        'voucher_api': {
            'handlers': ['debug-console'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['request_id'],
        },
    },
}
