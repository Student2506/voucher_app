LOG_FORMAT = (
    '%(asctime)s [%(levelname)s] [%(request_id)s - %(username)s] %(name) -30s %(funcName) -35s %(lineno) -5d:'
    '%(message)s'
)
LOG_DEFAULT_HANDLERS = ['debug-console', 'logstash']

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
        'logstash': {
            'level': 'INFO',
            'filters': ['require_debug_true', 'request_id'],
            'class': 'logstash.LogstashHandler',
            'host': 'logstash',
            'port': 5044,
            'fqdn': False,
            'tags': 'backend_front',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'INFO',
            'handlers': LOG_DEFAULT_HANDLERS,
            'propagate': False,
            'filters': ['request_id'],
        },
        'django': {
            'level': 'INFO',
            'handlers': LOG_DEFAULT_HANDLERS,
            'propagate': True,
            'filters': ['request_id'],
        },
        'django.request': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
            'propagate': False,
            'filters': ['request_id'],
        },
        'voucher_app': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
            'propagate': False,
            'filters': ['request_id'],
        },
        'voucher_api': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
            'propagate': False,
            'filters': ['request_id'],
        },
    },
}
