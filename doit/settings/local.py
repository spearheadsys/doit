from .base import *

SITE_URL = "http://127.0.0.1:8000/"
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS += (
    # 'debug_toolbar',
)

MIDDLEWARE += (
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doit',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
