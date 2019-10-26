import os
from os.path import basename, abspath, dirname

DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# print("django root: ")
# print(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)
# print("site name: ")
# print(SITE_NAME)

SETTINGS_DIR = os.path.join(DJANGO_ROOT, 'settings')
# print("settings_dir: ")
# print(SETTINGS_DIR)

# TEMPLATE_PATH = os.path.join(DJANGO_ROOT, '../templates')
# print("template_path: ")
# print(TEMPLATE_PATH)

STATIC_PATH = os.path.join(os.getcwd(), "static/")
# STATIC_PATH = os.path.join(DJANGO_ROOT, '../static')
# print("static_path: ")
# print(STATIC_PATH)
# STATIC_ROOT = os.path.join(DJANGO_ROOT, '../static/')
STATIC_ROOT = os.path.join(os.getcwd(), "static/")
# print("static root: ")
# print(STATIC_ROOT)
STATICFILES_DIRS = (
     # os.path.join(os.getcwd(), "static/"),
    # '/opt/local/share/httpd/htdocs/doit/doit/doit/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ADMINS = (
    ('Support', 'help@spearhead.systems'),
)

SECRET_KEY = 'generateYOURownsecretkeyhere'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []

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
    'django_mailbox',
    'taggit',
    'django_summernote',
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

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
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

DJANGO_MAILBOX_STORE_ORIGINAL_MESSAGE=True
DJANGO_MAILBOX_ATTACHMENT_UPLOAD_TO='uploads'

SUMMERNOTE_THEME = 'lite'
SUMMERNOTE_CONFIG = {
    'lang': None,
    'iframe': False,
    'summernote': {
        'airMode': False,
        'width': '100%',
        'height': '400',
        'disableDragAndDrop': False,
    },
    'toolbar': [
        ['style', ['bold', 'italic', 'underline', 'strikethrough', 'color']],
        ['para', ['ul', 'ol', 'paragraph', 'link']],
        ['insert', ['picture', 'video', 'table', 'hr']],
        ['misc', ['undo', 'redo']],
        ['insert', ['template']],
    ],
    # 'template': {
    #     'path': '/static/tpls/',
    #     'list': {
    #         'pending-close': 'Pending close'
    #     }
    # },
    'js': (
       '/static/js/summernote-ext-template.js',
    ),
    'js_for_inplace': (
        '/static/js/summernote-ext-template.js',
    ),
    'attachment_require_authentication': True,
    'disable_attachment': False,
    'lazy': False
}

# GIT master branch always points to the latest stable version
# Git development branch points to the current development version

# Set this to your outgoing address. Remeber to configure SPF/DKIM/DMARC accordingly
DOIT_MYEMAIL = 'help@spearhead.systems'
DOIT_VERSION = '0.0.4'
# set this to whatever default board you want for cards
# emails received will use this board as a default
DOIT_DEFAULT_BOARD = '1'
DATA_UPLOAD_MAX_MEMORY_SIZE = 1000000000
FILE_UPLOAD_MAX_MEMORY_SIZE = 1000000000
