from .common import Common


class Development(Common):
    ALLOWED_HOSTS = ['*']

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Common.INSTALLED_APPS + ['debug_toolbar']

    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + Common.MIDDLEWARE

    SECRET_KEY = 'secret_key'
