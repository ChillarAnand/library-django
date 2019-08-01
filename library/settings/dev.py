import airbrake
import dj_database_url
import os

from .base import *

SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']


DEVELOPMENT_APPS = (
    # 'debug_toolbar',
    # 'silk',
    'speedinfo',
)

INSTALLED_APPS += DEVELOPMENT_APPS


MIDDLEWARE_CLASSES = (
    'django_pdb.middleware.PdbMiddleware',
)


DEV_MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'speedinfo.middleware.ProfilerMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'querycount.middleware.QueryCountMiddleware',
    # 'django_pdb.middleware.PdbMiddleware',
]

MIDDLEWARE = DEV_MIDDLEWARE + MIDDLEWARE


INTERNAL_IPS = ALLOWED_HOSTS


QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 5,
        'HIGH': 10,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 1,
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': 1,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}


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

LOGGING = {}

try:
    AIRBRAKE_API_KEY = os.environ.get('AIRBRAKE_API_KEY')
    logger = airbrake.getLogger(api_key=AIRBRAKE_API_KEY, project_id=205620)
except:
    pass

# try:
#     1/0
# except Exception:
#     logger.exception("Bad math.")


# DATABASES = {
#     'default': dj_database_url.config(
#         default='postgres://f:f@localhost/library',
#         conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
#     )
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'library.db',
#         # 'NAME': '/Users/curatech/projects/library/library',
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'speedinfo.backends.proxy_cache',
        'CACHE_BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

print('dev')
print(DATABASES["default"]["NAME"])
print(DATABASES["default"])
print(DATABASES)
