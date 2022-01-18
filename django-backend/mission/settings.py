"""
Django settings for iron project.

Generated by 'django-admin startproject' using Django 2.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path
import sys
import json

path = '/mnt/appconfig.json'
if os.path.exists(path):
    with open(path) as f:
        app_config = json.load(f)
        for key in app_config:
            os.environ[key] = str(app_config[key])

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for key in soarcast_config:
    os.environ[key] = soarcast_config[key]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!mc2c_)nstii!k+5o8wki4qg_o76%h8s%vp_)z4*lpe((4st-x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG', 'false').lower() in ('1', 'true') else False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_otp',
    'django_otp.plugins.otp_totp',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'user_profile',
    'django_celery_beat',
    'saltmaster',
    'app',
    'notifications',
    'drf_yasg2',
    'django_filters',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'user_profile.middleware.MFAdMiddleware',
]

ROOT_URLCONF = 'mission.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mission.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# Get Production Settings
from configparser import ConfigParser
MISSION_CONFIG = '/etc/mission/mission.conf'
parser = ConfigParser(interpolation=None)
parser.read(MISSION_CONFIG)

#LOG_DIR = BASE_DIR
#if 'mod_wsgi' in parser:
#wsgi = parser['mod_wsgi']
DOMAIN_URL = os.getenv('DOMAIN_URL')
FRONTEND_URL = os.getenv('FRONTEND_URL')


LOG_DIR = '/var/log/soarcast'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("POSTGRES_DB"),
        'USER':  os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT")
    }
}

# configure Vault
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
VAULT_HOST = os.getenv('VAULT_HOST', 'http://127.0.0.1:8200')
VAULT_ROOT_PATH = os.getenv('VAULT_ROOT_PATH', 'soarcast')
VAULT_VERIFY_CERTIFICATE = os.getenv('VAULT_VERIFY_CERTIFICATE', False)
TOKEN_LIFE_TIME = os.getenv('TOKEN_LIFE_TIME') #days


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_EMAIL_SETTINGS = {
    'host': os.getenv('EMAIL_HOST'),
    'port': os.getenv('EMAIL_PORT'),
    'username': os.getenv('EMAIL_USERNAME'),
    'password': os.getenv('EMAIL_PASSWORD'),
    'use_tls': os.getenv('USE_TLS'),
    'use_ssl': os.getenv('USE_SSL'),
    'email_from': os.getenv('EMAIL_FROM'),
}


REDIS_USER = os.getenv('REDIS_USER')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_SSL = False if not os.getenv('REDIS_SSL') or os.getenv('REDIS_SSL') == '0' else True
REDIS_VERIFY_SSL = False if not os.getenv('REDIS_VERIFY_SSL') or os.getenv('REDIS_VERIFY_SSL') == '0' else True


# CELERY Settings
if os.getenv('REDIS_SSL'):
    BROKER_URL = f'rediss://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}?ssl_cert_reqs=none'
else:
    BROKER_URL = f'redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = BROKER_URL
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'US/Eastern'


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'app.authentication.HashedTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Logging Settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {

        'production_log': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'saltmaster_log': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'app_log': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'django': {
            'handlers': ['production_log']
        },
        'saltmaster': {
            'handlers': ['saltmaster_log'],
            'level': 'DEBUG',
        },
        'app': {
            'handlers': ['app_log'],
            'level': 'DEBUG',
        },
    }
}
MODULES_PATH = '/var/cache/salt/minion/extmods/modules/'


from datetime import timedelta
SIMPLE_JWT = {
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.SlidingToken',),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
LOGIN_URL = '/login/'
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.soarcast\.io$",
    r"^https://\w+\.\w+\.soarcast\.io$",
    r"^http://\w+\.soarcast\.io$",
    r"^http://\w+\.\w+\.soarcast\.io$",
    r"^https://soarcast\.\w+\.\w+$",
]
CORS_ALLOWED_ORIGINS = [

]
