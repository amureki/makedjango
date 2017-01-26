from configurations import values

from .common import Common


class Production(Common):
    ALLOWED_HOSTS = []

    CSRF_COOKIE_SECURE = True

    DEBUG = False

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'simple': {'format': '[%(name)s] %(levelname)s: %(message)s'},
            'full': {'format': '%(asctime)s [%(name)s] %(levelname)s: %(message)s'},
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },

        },
    }

    MIDDLEWARE = ['django.middleware.http.ConditionalGetMiddleware',
                  'django.middleware.gzip.GZipMiddleware', ] + Common.MIDDLEWARE

    SECRET_KEY = values.SecretValue()

    SECURE_BROWSER_XSS_FILTER = True

    SESSION_COOKIE_SECURE = True
