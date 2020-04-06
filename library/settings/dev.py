import os
from pprint import pprint

import airbrake
import dj_database_url
from django.db.models.functions import Cast

from .base import *

SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1', '*']
# ALLOWED_HOSTS = ['*']


DEVELOPMENT_APPS = (
    # 'autofixture',
    'debug_toolbar',
    # 'silk',
    # 'speedinfo',
    # 'django_json_widget',
    # 'xadmin',
    # 'djadmin2',
    'django_otp',
    'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',
    # 'two_factor',
    # 'elasticapm.contrib.django',
)


INSTALLED_APPS += DEVELOPMENT_APPS
print(INSTALLED_APPS)

MIDDLEWARE_CLASSES = (
    'django_pdb.middleware.PdbMiddleware',
)

DEV_MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'speedinfo.middleware.ProfilerMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 'querycount.middleware.QueryCountMiddleware',
    # 'django_pdb.middleware.PdbMiddleware',
]

SILK_ENABLED = 'silk' in INSTALLED_APPS

if SILK_ENABLED:
    DEV_MIDDLEWARE.append(
        'silk.middleware.SilkyMiddleware',
    )

# MIDDLEWARE = MIDDLEWARE + DEV_MIDDLEWARE
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
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5959,
            'version': 1,
            'message_type': 'logstash',
            'fqdn': True,
            'tags': ['library'],
        }

    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console', 'logstash'],
        },
         'django.request': {
            'handlers': ['logstash'],
            'level': 'DEBUG',
            'propagate': True,
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
#         default=os.getenv('DATABASE_URL'),
#         conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600)),
#     )
# }

CACHES = {
    'default': {
        'BACKEND': 'speedinfo.backends.proxy_cache',
        'CACHE_BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

print('dev')
# print(DATABASES["default"]["NAME"])

import decimal
# from speedinfo.settings import ReportColumnFormat, DEFAULTS
from django.db.models import F, ExpressionWrapper, FloatField, Max, Value
from django.db.models.functions import Greatest

# SPEEDINFO_REPORT_COLUMNS = [
#     'impact_factor']
# SPEEDINFO_REPORT_COLUMNS_FORMAT = [
#     ReportColumnFormat(
#         'impact factor',
#         '{:.4f}',
#         '',
#         ExpressionWrapper(100.0 * F('anon_calls') / F('total_calls'), output_field=FloatField())
#     )
# ]

from django.db.models import FloatField, ExpressionWrapper, F, Func

template = '%(function)s%(expressions)s over()::numeric'
fv2 = Func(Max('total_time'), function='', template=template)

# DEFAULTS['SPEEDINFO_REPORT_COLUMNS'] += ('impact_factor',)
# DEFAULTS['SPEEDINFO_REPORT_COLUMNS_FORMAT'].append(
#     ReportColumnFormat(
#         'Impact Factor',
#         '{:.2f}',
#         'impact_factor',
#         ExpressionWrapper(
#             F('total_time') / fv2,
#             output_field=FloatField()
#         )
#     )
# )
pprint(DATABASES["default"])
# pprint(DATABASES)

# ELASTIC_APM = {
#     'SERVICE_NAME': 'library',
#     'SECRET_TOKEN': 'library',
#     'DEBUG': True,
# }

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = '/tmp/'
print(DEBUG)

# INSTALLED_APPS += ('controlcenter',)
# CONTROLCENTER_DASHBOARDS = (
#     ('bookdash', 'book.dashboard.BookDashboard'),
# )

# INSTALLED_APPS += ('admin_honeypot',)

OTP_TOTP_ISSUER = 'Library Inc.'

# INSTALLED_APPS += ('jet_django',)
# JET_PROJECT = 'library'
# JET_TOKEN = os.environ.get('JET_TOKEN')

INSTALLED_APPS += ('advanced_filters',)
# pprint(INSTALLED_APPS)
