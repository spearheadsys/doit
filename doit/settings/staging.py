from .base import *

SITE_URL = "http://dev.doit.spearhead.systems/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doit',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

#EMAIL_HOST = 'localhost'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
