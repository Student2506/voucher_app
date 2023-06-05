"""Logging description (settings)."""

LOG_FORMAT = (
    '%(asctime)s [%(levelname)s] [%(request_id)s - %(username)s] %(name) -30s %(funcName) -35s %(lineno) -5d: '
    '%(message)s'
)
LOG_DEFAULT_HANDLERS = ['console', 'logstash']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'request_id': {
            '()': 'log_filters.filters.RequestIdFilter',
        },
    },
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
        },
        'default': {
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['request_id'],
        },
        'logstash': {
            'level': 'INFO',
            'filters': ['request_id'],
            'class': 'logstash.LogstashHandler',
            'host': 'logstash',
            'port': 5044,
            'fqdn': False,
            'tags': ['backend'],
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'DEBUG',
        },
        'fontTools.*': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'WARNING',
        },
    },
    'root': {
        'level': 'DEBUG',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
