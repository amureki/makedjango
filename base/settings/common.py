import os
from pathlib import Path

import django_cache_url

from configurations import Configuration, values


class Common(Configuration):
    PROJECT_PACKAGE = Path(__file__).resolve().parent.parent

    BASE_DIR = PROJECT_PACKAGE.parent

    ALLOWED_HOSTS = []

    CACHES = {
            'default': django_cache_url.parse(
                os.getenv('CACHE_URL', 'locmem://cache')
            ),
            'sessions': django_cache_url.parse(
                os.getenv('SESSIONS_URL', 'locmem://sessions')
            ),
        }

    DATABASES = values.DatabaseURLValue(
        default='postgres://localhost/{{ project_name }}',
        # django-configurations maps this to the caster (which is dj_database_url)
        conn_max_age=500,
    )

    DEBUG = True

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.humanize',
        'django.contrib.admin',
        'django.contrib.postgres',

        'django_extensions',
    ]

    LANGUAGE_CODE = 'en-us'

    MEDIA_URL = values.Value(default='/media/', environ_prefix='')
    MEDIA_ROOT = os.path.join(BASE_DIR, '_media')

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    ]

    ROOT_URLCONF = 'base.urls'

    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'

    SITE_ID = 1

    STATIC_URL = values.Value(default='/static/', environ_prefix='')
    STATIC_ROOT = os.path.join(BASE_DIR, '_static')

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.static',
                    'django.template.context_processors.media',
                    'django.contrib.messages.context_processors.messages',
                    "django.template.context_processors.request",
                    "django.template.context_processors.tz",
                    "django.template.context_processors.csrf",
                ],
            },
        },
    ]

    TIME_ZONE = 'Europe/Berlin'

    USE_I18N = True

    USE_L10N = False

    USE_TZ = True

    WSGI_APPLICATION = 'base.wsgi.application'
