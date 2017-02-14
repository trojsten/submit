# Django settings for example project.

import os
from django.contrib.messages import constants as message_constants


PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(
    os.path.dirname(os.path.abspath(__file__))
)


def env(name, default):
    return os.environ.get(name, default)

DEBUG = True

SECRET_KEY = '-(tu4#dd!-9x9fmxvsq*psm^1+e+=r@ofes&6tk*e-gpk5mhn9'

SENDFILE_BACKEND = 'sendfile.backends.development'

THUMBNAIL_DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrapform',
    'example',
    'submit',
    'example.tasks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = { 
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'submit_example',
        'USER': 'submit_example',
        'PASSWORD': '',
    },
}


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sk-SK'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Bratislava'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'locale'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, PROJECT_MODULE_NAME, 'static')

AUTH_USER_MODEL = 'auth.User'

# Bootstrap classes for messages
MESSAGE_TAGS = {
    message_constants.DEBUG: 'alert-debug',
    message_constants.INFO: 'alert-info',
    message_constants.SUCCESS: 'alert-success',
    message_constants.WARNING: 'alert-warning',
    message_constants.ERROR: 'alert-danger',
}

# Task statements
TASKS_DEFAULT_SUBMIT_RECEIVER_TEMPLATE = 'source'

# Submit app
SUBMIT_POST_SUBMIT_FORM_VIEW = 'example.submit_configuration.PostSubmitFormCustomized'
#SUBMIT_PREFETCH_DATA_FOR_SCORE_CALCULATION = 'example.submit_configuration.prefetch_data_for_score_calculation'
#SUBMIT_DISPLAY_SCORE = 'example.submit_configuration.display_score'
JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER = 'example.submit_configuration.default_inputs_folder_at_judge'
SUBMIT_CAN_POST_SUBMIT = 'example.submit_configuration.can_post_submit'

SUBMIT_TASK_MODEL = 'tasks.Task'
SUBMIT_PATH = env('SUBMIT_PATH', os.path.join(PROJECT_DIR, 'submit'))
JUDGE_INTERFACE_IDENTITY = env('JUDGE_INTERFACE_IDENTITY', 'EXAMPLE')
JUDGE_ADDRESS = env('JUDGE_ADDRESS', '127.0.0.1')
JUDGE_PORT = int(env('JUDGE_PORT', 12347))

# Debug toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INSTALLED_APPS += (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES = (
    ('debug_toolbar.middleware.DebugToolbarMiddleware',) +
    MIDDLEWARE_CLASSES
)
INTERNAL_IPS = ('127.0.0.1',)
