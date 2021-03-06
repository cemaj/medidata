from .common import *

ALLOWED_HOSTS.append('medi.mohub.co')
ALLOWED_HOSTS.append('web02-cl02-mde.flexiion-customer.net')

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'medi',
        'USER': 'medi',
        'PASSWORD': 'medi',
        'HOST': 'db',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'raven': {
            'level': 'ERROR',
            'handlers': ['sentry','console'],
            'propagate': False,
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['sentry','console'],
            'propagate': False,
        },
    }
}

EMIS_API_HOST = 'http://medi2data.net:9443'
