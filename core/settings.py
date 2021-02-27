from pathlib import Path

import environ
import sentry_sdk
from configurations import Configuration, values
from django.urls import reverse_lazy
from sentry_sdk.integrations.django import DjangoIntegration

env = environ.Env()


class Common(Configuration):
    PROJECT_ROOT = Path(__file__).resolve(strict=True).parent
    BASE_DIR = PROJECT_ROOT.parent

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
        "django.contrib.sites",
        "django.contrib.humanize",

        'django_extensions',

        'core',
        'users',
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

    ROOT_URLCONF = 'core.urls'

    SECRET_KEY = values.SecretValue()

    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'

    SITE_ID = 1
    SITE_URL = env("SITE_URL", default="https://example.com/")

    STATIC_ROOT = BASE_DIR / "_static"
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "django.template.context_processors.csrf",
                ],
            },
        },
    ]

    TIME_ZONE = 'Europe/Berlin'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    WSGI_APPLICATION = 'core.wsgi.application'

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

    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=""),
        integrations=[DjangoIntegration()],
    )


class Development(Common):
    ALLOWED_HOSTS = ["*"]
    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Common.INSTALLED_APPS + ['debug_toolbar']
    INTERNAL_IPS = ("127.0.0.1",)

    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + Common.MIDDLEWARE
    SECRET_KEY = "secret_key"


class Test(Common):
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    EMAIL_BACKEND = "common.mail.backend.LocmemEmailBackend"

    SECRET_KEY = Development.SECRET_KEY


class Production(Common):
    ALLOWED_HOSTS = values.ListValue(environ_prefix="", default=[])

    MIDDLEWARE = [
        "django.middleware.http.ConditionalGetMiddleware",
        "django.middleware.gzip.GZipMiddleware",
    ] + Common.MIDDLEWARE

    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # see https://docs.djangoproject.com/en/dev/ref/middleware/#http-strict-transport-security
    SECURE_HSTS_SECONDS = values.IntegerValue(environ_prefix="", default=3600)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
