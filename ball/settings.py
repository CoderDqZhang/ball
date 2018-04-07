"""
Django settings for ball project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '52*p4fl8e0s4^6uwpyvuif!*(@3=olqda6rvwnurvgv%2h(rvn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'

import os
STATIC_PATH = os.path.join( os.path.dirname(__file__) , 'static' )

MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'
# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'ball',
    'mycode',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.middleware.common.CommonMiddleware',
# # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
# # 'django.contrib.auth.middleware.AuthenticationMiddleware',
#
#     # 'django.middleware.csrf.CsrfViewMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

ROOT_URLCONF = 'ball.urls'

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

WSGI_APPLICATION = 'ball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ball',
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'innodb': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': { 'init_command': 'SET default_storage_engine=INNODB;' }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson",
 }

GEOS_LIBRARY_PATH = '/home/bob/local/lib/libgeos_c.so'



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# -*- coding: utf-8 -*-
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#             'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
#     # logging formater
#     },
#     'filters': {
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'include_html': True,
#         },
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/Users/zhang/Documents/Python/ball/logs/all.log',  # log out put file
#             'maxBytes': 1024 * 1024 * 5,  # log size
#             'backupCount': 5,  # log count
#             'formatter': 'standard',  # log formatters type
#         },
#         'error': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/Users/zhang/Documents/Python/ball/logs/error.log',
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 5,
#             'formatter': 'standard',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'standard'
#         },
#         'request_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/Users/zhang/Documents/Python/ball/logs/request.log',
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 5,
#             'formatter': 'standard',
#         },
#         'scprits_handler': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/Users/zhang/Documents/Python/ball/logs/scprits.log',
#             'maxBytes': 1024 * 1024 * 5,
#             'backupCount': 5,
#             'formatter': 'standard',
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['default', 'console'],
#             'level': 'DEBUG',
#             'propagate': False
#         },
#         'django.request': {
#             'handlers': ['request_handler'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'scripts': {
#             'handlers': ['scprits_handler'],
#             'level': 'INFO',
#             'propagate': False
#         },
#         'ball.webdns.views': {
#             'handlers': ['default', 'error'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         'ball.webdns.util': {
#             'handlers': ['error'],
#             'level': 'ERROR',
#             'propagate': True
#         }
#     }
# }