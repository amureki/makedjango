from .common import Common


class Test(Common):
    DEBUG = False

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    SECRET_KEY = 'secret_key'
