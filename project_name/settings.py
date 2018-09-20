import os
from pathlib import Path

import environ
from configurations import Configuration, values

env = environ.Env()


class Common(Configuration):
    PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

    BASE_DIR = PROJECT_PACKAGE.parent

    ALLOWED_HOSTS = []

    CACHES = {
        'default': env.cache('CACHE_URL', 'redis://127.0.0.1:6379/0'),
        'sessions': env.cache('SESSIONS_URL', 'redis://127.0.0.1:6379/1'),
    }

    DATABASES = {
        'default': env.db(default='postgres://localhost/{{ project_name }}?conn_max_age=500'),
    }

    DEBUG = False

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.postgres',
        'django.contrib.staticfiles',

        'django_extensions',

        '{{ project_name }}.users',
    ]

    LANGUAGE_CODE = 'en-us'

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = '{{ project_name }}.urls'

    SECRET_KEY = values.SecretValue()

    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '_static')

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    "django.template.context_processors.request",
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    "django.template.context_processors.csrf",
                ],
            },
        },
    ]

    TIME_ZONE = 'Europe/Berlin'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

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

    AUTH_USER_MODEL = 'users.User'


class Development(Common):
    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Common.INSTALLED_APPS + ['debug_toolbar']

    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + Common.MIDDLEWARE


class Test(Common):
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    SECRET_KEY = 'secret_key'


class Production(Common):
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True

    MIDDLEWARE = [
        'django.middleware.http.ConditionalGetMiddleware',
        'django.middleware.gzip.GZipMiddleware',
    ] + Common.MIDDLEWARE
