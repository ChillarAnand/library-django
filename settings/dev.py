# flake8: NOQA
from .base import *


SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = True

ALLOWED_HOSTS = ['*', ]


INSTALLED_APPS += (
    'django_extensions',
)


LOGGING = {
    'version': 1,
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
}

LOGGING = None
