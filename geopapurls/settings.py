import dj_database_url
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DEBUG = bool(os.environ.get('DEBUG', False))
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
SERVER_EMAIL = None
MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
    'django.core.context_processors.tz',
    'django.core.context_processors.static'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'geopapurls.urls'

WSGI_APPLICATION = 'geopapurls.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "geopapurls", "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'south',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'crispy_forms',
    'django.contrib.admin',
    'geopapurls',
)

EMAIL_HOST = ''
EMAIL_PORT = 25
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD =None

LOGGING = {}

DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}

LOGIN_URL = os.environ['LOGIN_URL']
LOGOUT_NEXT_PAGE = os.environ['LOGOUT_NEXT_PAGE']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split()
SECRET_KEY = os.environ['SECRET_KEY']
CRISPY_TEMPLATE_PACK = 'bootstrap3'
MAX_RESULTS_PER_PAGE = int(os.environ['MAX_RESULTS_PER_PAGE'])

try:
    from local_settings import *
except:
    pass
