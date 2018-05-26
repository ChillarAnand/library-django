from .base import *


SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']


DEVELOPMENT_APPS = (
    'django_extensions',
    'debug_toolbar',
)

INSTALLED_APPS += DEVELOPMENT_APPS


MIDDLEWARE_CLASSES = (
    'django_pdb.middleware.PdbMiddleware',
)


DEV_MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'querycount.middleware.QueryCountMiddleware',
    'django_pdb.middleware.PdbMiddleware',
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
