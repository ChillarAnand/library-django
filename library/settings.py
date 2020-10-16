import os
from pprint import pprint
import os
from pprint import pprint

import airbrake
import dj_database_url
from django.db.models.functions import Cast



env = os.environ.get

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(BASE_DIR)

SECRET_KEY = 'q6emagfzaeftr*4$o@@608v3!)(^cmvwm@2kcatu7if(c#0w+@'

DEBUG = bool(os.environ.get('DEBUG', 'True'))

ALLOWED_HOSTS = ['0.0.0.0', '.heroku.com', ]

INSTALLED_APPS = (
    # 'object_tools',
    # 'admin_menu',
    'django.contrib.admin',
    # 'library.apps.LibraryAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 'oauth2_provider',
    # 'channels',

    'rest_framework',
    'drf_generators',
    'django_extensions',
    # 'django_celery_results',

    # our apps
    'book',
    'crm',
    'chat',
    'trash',
)

# ADMIN_STYLE = {
#     'primary-color': '#417690',
#     'secondary-color': '#79aec8',
#     'tertiary-color': '#c4dce8'
# }

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

pprint(TEMPLATES)

WSGI_APPLICATION = 'library.wsgi.application'

DATABASES = {
    'default': dj_database_url.config()
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
STATIC_ROOT = 'static'
# print(STATICFILES_DIRS)

# MEDIA_ROOT = os.path.join(BASE_DIR)
MEDIA_ROOT = BASE_DIR
MEDIA_URL = '/media/'


ASGI_APPLICATION = "library.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


TEST = True
CELERY_RESULT_BACKEND = 'django-db'


SECRET_KEY = os.environ.get('SECRET_KEY', 'dummy')
ALLOWED_HOSTS = ['*']


DEVELOPMENT_APPS = (
    # 'autofixture',
    'debug_toolbar',
    'silk',
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


CACHES = {
    'default': {
        'BACKEND': 'speedinfo.backends.proxy_cache',
        'CACHE_BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

print('dev')

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

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.environ.get('SENTRY_DSN')
VERSION = os.environ.get('VERSION')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        release=VERSION,
    )
