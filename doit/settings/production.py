# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from .base import *

SITE_URL = "http://127.0.0.1:8000"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(os.getcwd(), "media/")

STATIC_PATH = os.path.join(DJANGO_ROOT, 'static')
# print("static_path: ")
# print(STATIC_PATH)

STATICFILES_DIRS = (
    STATIC_PATH,
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'production',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# we reun gunicorn/nginx in production
USE_X_FORWARDED_HOST = True