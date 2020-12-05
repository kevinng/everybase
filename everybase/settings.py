"""
Django settings for everybase project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
import django_heroku
import dj_database_url
from django.contrib.messages import constants as messages
from django.conf.locale.en import formats as en_formats

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'relationships.apps.RelationshipsConfig',
    'communication.apps.CommunicationConfig',
    'files.apps.FilesConfig',
    'leads.apps.LeadsConfig',
    'growth.apps.GrowthConfig',
    'lander.apps.LanderConfig',
    'django_filters',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'everybase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'everybase.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {}
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('PSQL_NAME'),
        'USER': config('PSQL_USER'),
        'PASSWORD': config('PSQL_PASSWORD'),
        'HOST': config('PSQL_HOST'),
        'PORT': config('PSQL_PORT')
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Activate Django-Heroku.
django_heroku.settings(locals())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Override message tags
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Celery-related configurations

if 'REDIS_URL' in os.environ:
    CELERY_BROKER_URL = config('REDIS_URL')
else:
    CELERY_BROKER_URL = 'redis://%s:%s' % (
        config('REDIS_HOST'),
        config('REDIS_PORT')
    )

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'schedule-load-gmass-campaign-main-report': {
        'task': 'growth.tasks.update_gmass_data',
        'schedule': 43200.0 # 12-hour interval
    }
}

# Email-related configurations

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
# System email sender
EMAIL_SYS_SENDER_EMAIL_ADDRESS = 'system@everybase.co'
# System email receivers
EMAIL_SYS_RECEIVER_EMAIL_ADDRESSES = ['system@everybase.co']

if DEBUG == False:
    # Force HTTPS only
    SECURE_SSL_REDIRECT = True

    # Required for Heroku
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = '/login'

AWS_REGION_NAME = config('AWS_REGION')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_PRESIGNED_URL_EXPIRES_IN = config('AWS_PRESIGNED_URL_EXPIRES_IN')

# Root for all files uploaded via the 'files' app.
AWS_S3_FILES_ROOT = 'files'

# List of persons to notify when someone signs up as a lead
LEAD_SIGN_UP_NOTIFICATION_LIST = ['kevin@everybase.co']

# Django administration default datetime format
en_formats.DATETIME_FORMAT = 'd M Y H:i:s'

# Increase maximum number of fields allowable in a form for bulk upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000

# System timestamps keys - of timestamps to track in the system
SYSTS_LAST_UPDATED_GMASS_BOUNCES = 'GMASS_BOUNCES'
SYSTS_LAST_UPDATED_GMASS_UNSUBSCRIBES = 'GMASS_UNSUBSCRIBES'