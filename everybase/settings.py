"""
Django settings for everybase project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sentry_sdk
import django_heroku
import dj_database_url

from decouple import config
from django.contrib.messages import constants as messages
from django.conf.locale.en import formats as en_formats
from sentry_sdk.integrations.django import DjangoIntegration

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common.apps.CommonConfig',
    'relationships.apps.RelationshipsConfig',
    'chat.apps.ChatConfig',
    'files.apps.FilesConfig',
    'growth.apps.GrowthConfig',
    'amplitude.apps.AmplitudeConfig',
    'leads.apps.LeadsConfig',
    'django_filters',
    'django_extensions',
    'widget_tweaks',
    'rest_framework',
    'storages',
    'django_user_agents',
    'phonenumber_field',
    'loginas',
    'payments.apps.PaymentsConfig'
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware'
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
                'django_settings_export.settings_export'
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

AUTHENTICATION_BACKENDS = [
    # Required for admin backend to work
    'django.contrib.auth.backends.ModelBackend',

    # Supports passwordless login to work
    'relationships.auth.backends.DirectBackend',
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

# Custom AWS settings
AWS_REGION_NAME = config('AWS_REGION')
AWS_PRESIGNED_URL_EXPIRES_IN = config('AWS_PRESIGNED_URL_EXPIRES_IN')
# django-storages AWS settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
# See: https://stackoverflow.com/questions/48722355/aws-s3-and-django-returns-an-error-occurred-accessdenied-when-calling-the-put
AWS_DEFAULT_ACL = None

# Media URL
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Root for all files uploaded via the 'files' app.
AWS_S3_FILES_ROOT = 'files'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static folder relative to app
STATIC_URL = '/static/'

# Static files that aren't tied to apps
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# Notes:
#   - Use whitenoise for development, but AWS S3 for production
#   - We only use django-storages to help use collectstatic assets, not upload
#       or manage media from users
STATICFILES_STORAGE = config('STATICFILES_STORAGE')
DEFAULT_FILE_STORAGE = 'everybase.storage_backends.MediaStorage'
AWS_S3_KEY_STATUS_IMAGE = 'statuses/%s/%s' # User ID, file ID
AWS_S3_KEY_STATUS_IMAGE_THUMBNAIL = 'statuses/%s/t/%s' # User ID, file ID
STATUS_IMAGE_THUMBNAIL_SIZE = 300, 200
MAX_STATUS_IMAGES = 12
MAX_STATUS_IMAGE_FILE_SIZE_IN_BYTES = 1048576
AWS_S3_KEY_REVIEW_IMAGE = 'reviews/%s/%s/%s' # Phone number ID, reviewer ID, file ID
AWS_S3_KEY_REVIEW_IMAGE_THUMBNAIL = 'reviews/%s/%s/t/%s' # Phone number ID, reviewer ID, file ID
REVIEW_IMAGE_THUMBNAIL_SIZE = 300, 200
MAX_REVIEW_IMAGES = 12
MAX_REVIEW_IMAGE_FILE_SIZE_IN_BYTES = 1048576

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
    # 'schedule-load-gmass-campaign-main-report': {
    #     'task': 'growth.tasks.update_gmass_data',
    #     'schedule': 43200.0 # 12-hour interval
    # }
}

# Email-related configurations

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
# System email sender
EMAIL_SYS_SENDER_EMAIL_ADDRESS = config('SYSTEM_EMAIL')
# System email receivers
EMAIL_SYS_RECEIVER_EMAIL_ADDRESSES = [config('SYSTEM_EMAIL')]

if DEBUG == False:
    # Force HTTPS only
    SECURE_SSL_REDIRECT = True

    # Required for Heroku
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = '/login'

# Django administration default datetime format
en_formats.DATETIME_FORMAT = 'd M Y H:i:s'

# Increase maximum number of fields allowable in a form for bulk upload
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000

# System timestamps keys - of timestamps to track in the system
SYSTS_LAST_UPDATED_GMASS_BOUNCES = 'GMASS_BOUNCES'
SYSTS_LAST_UPDATED_GMASS_UNSUBSCRIBES = 'GMASS_UNSUBSCRIBES'

# Twilio
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_WEBHOOK_INCOMING_MESSAGES_URL = \
    config('TWILIO_WEBHOOK_INCOMING_MESSAGES_URL')
TWILIO_WEBHOOK_STATUS_UPDATE_URL = \
    config('TWILIO_WEBHOOK_STATUS_UPDATE_URL')

# Hash ID Field
HASHID_FIELD_SALT = config('HASHID_FIELD_SALT')
HASHID_FIELD_MIN_LENGTH = config('HASHID_FIELD_MIN_LENGTH')

# System base URL
BASE_URL = config('BASE_URL')

# Stripe
STRIPE_ENDPOINT_SECRET = config('STRIPE_ENDPOINT_SECRET')
STRIPE_SECRET_API_KEY = config('STRIPE_SECRET_API_KEY')
STRIPE_PUBLISHABLE_API_KEY = config('STRIPE_PUBLISHABLE_API_KEY')
STRIPE_PAYMENT_METHOD_TYPES = config('STRIPE_PAYMENT_METHOD_TYPES').split(';')

# User-facing chatbot user and phone number
CHATBOT_USER_PK = config('CHATBOT_USER_PK')

sentry_sdk.init(
    dsn="https://b66301735a0345b3b7c6bee436d28bb7@o870163.ingest.sentry.io/5824419",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Missive's URL for Twilio WhatsApp incoming message and status update
# callbacks. We copy such post requests to Missive so we may manage it there.
MISSIVE_TWILIO_WA_CALLBACK_URL = config('MISSIVE_TWILIO_WA_CALLBACK_URL')

AMPLITUDE_API_KEY = config('AMPLITUDE_API_KEY')
AMPLITUDE_SECRET_KEY = config('AMPLITUDE_SECRET_KEY')
AMPLITUDE_SESSION_TIMEOUT_SECONDS = config('AMPLITUDE_SESSION_TIMEOUT_SECONDS')
AMPLITUDE_IDENTIFY_URL = config('AMPLITUDE_IDENTIFY_URL')

GMASS_CAMPAIGN_UPDATE_TIMEFRAME_DAYS = config('GMASS_CAMPAIGN_UPDATE_TIMEFRAME_DAYS')

ADMIN_PATH = str(config('ADMIN_PATH')).strip()

# Login/register tokens expiry duration in seconds
# LOGIN_TOKEN_EXPIRY_SECS = 900 # 15 minutes
# REGISTER_TOKEN_EXPIRY_SECS = 900 # 15 minutes

# S3 path for lead files
LEADS_FILES_S3_PATH = 'leads'

RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')
RECAPTCHA_VERIFICATION_URL = config('RECAPTCHA_VERIFICATION_URL')
RECAPTCHA_THRESHOLD = config('RECAPTCHA_THRESHOLD')

# Google Analytics 4 settings
GA_WEB_STREAM_ID = config('GA_WEB_STREAM_ID')

# Facebook App ID
FACEBOOK_APP_ID = config('FACEBOOK_APP_ID')

# Export parameters that can be used in templates
SETTINGS_EXPORT = [
    'BASE_URL',
    'GA_WEB_STREAM_ID',
    'RECAPTCHA_SITE_KEY',
    'AMPLITUDE_API_KEY',
    'FACEBOOK_APP_ID',
    'MAX_STATUS_IMAGES',
    'MAX_STATUS_IMAGE_FILE_SIZE_IN_BYTES',
    'MAX_REVIEW_IMAGES',
    'MAX_REVIEW_IMAGE_FILE_SIZE_IN_BYTES'
]

# 5 MB 5242880
MAX_UPLOAD_SIZE = 5242880

# Confirmation codes - e.g., login email/WhatsApp code - resend interval in seconds
CONFIRMATION_CODE_RESEND_INTERVAL_SECONDS = int(config('CONFIRMATION_CODE_RESEND_INTERVAL_SECONDS'))
CONFIRMATION_CODE_EXPIRY_SECONDS = int(config('CONFIRMATION_CODE_EXPIRY_SECONDS'))

DEFAULT_AUTO_FIELD='django.db.models.AutoField'