import os

import airbrake

from .base import *


SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = False

ALLOWED_HOSTS = ['*']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },

    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            # 'handlers': ['console', ],
        },
    }
}

AIRBRAKE_API_KEY = os.environ.get('AIRBRAKE_API_KEY')


logger = airbrake.getLogger(api_key=AIRBRAKE_API_KEY, project_id=205620)

try:
    1/0
except Exception:
    logger.exception("Bad math.")
