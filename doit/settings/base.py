import os
from os.path import basename, abspath, dirname

SITE_URL = "http://127.0.0.1:8000/"
X_FRAME_OPTIONS = 'SAMEORIGIN'
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_NAME = basename(DJANGO_ROOT)
SETTINGS_DIR = os.path.join(DJANGO_ROOT, 'settings')
STATIC_PATH = os.path.join(os.getcwd(), "doit/static/")
STATIC_ROOT = os.path.join(os.getcwd(), "static/")
STATICFILES_DIRS = (
     STATIC_PATH,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMINS = (
    ('Support', 'help@spearhead.systems'),
)

SECRET_KEY = 'generateYOURownsecretkeyhere'
DEBUG = False


# Application definition
INSTALLED_APPS = (
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'card',
    'contact',
    'organization',
    'board',
    'report',
    'attachment',
    'comment',
    'doit',
    'bootstrap3_datetime',
    'django.contrib.humanize',
    'taggit',
    'rest_framework',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'card.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'doit.urls'
WSGI_APPLICATION = 'doit.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.getcwd(), "media/")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(DJANGO_ROOT, '../templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ]
        },
    },
]

INTERNAL_IPS = ('127.0.0.1')
LOGIN_URL = '/login/'
AUTH_PROFILE_MODULE = "contact.UserProfile"
# TAGGIT_CASE_INSENSITIVE = True

# Set this to your outgoing address. Remeber to configure SPF/DKIM/DMARC accordingly
DOIT_MYEMAIL = 'help@spearhead.systems'
DOIT_VERSION = '0.0.4'
# set this to whatever default board you want for cards (id)
# emails received will use this board as a default unless
# sender is identified correctly and assigned to default_board
# of said organization (if it exists)
DOIT_DEFAULT_BOARD = '1'
DATA_UPLOAD_MAX_MEMORY_SIZE = 1000000000
FILE_UPLOAD_MAX_MEMORY_SIZE = 1000000000
