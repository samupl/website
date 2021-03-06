"""
Django settings for website project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'website.conf'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secret', 'key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug', 'debug')

ALLOWED_HOSTS = ['samu.pl']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'bootstrap3',
    'captcha',
    'django_gravatar',
    # Website apps
    'apps.hexencoder',
    'apps.pages',
    'apps.contact',
    'apps.blog',
    'apps.keybase',
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

ROOT_URLCONF = 'website.urls'

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

WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'engine'),
        'NAME': os.path.join(BASE_DIR, config.get('database', 'name'))
        if config.get('database', 'engine').endswith('sqlite3')
        else config.get('database', 'name'),
        'USER': config.get('database', 'user'),
        'PASSWORD': config.get('database', 'password'),
        'HOST': config.get('database', 'host'),
        'PORT': config.get('database', 'port'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'media'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CAPTCHA_NOISE_FUNCTIONS = [
    'captcha.helpers.noise_arcs',
    'captcha.helpers.noise_dots'
]

RECAPTCHA_PUBLIC_KEY = config.get('captcha', 'public_key')
RECAPTCHA_PRIVATE_KEY = config.get('captcha', 'private_key')
NOCAPTCHA = True


# Contact form
CONTACT_FORM_RCPT = config.get('contact_form', 'rcpt')
CONTACT_FORM_SUBJECT_PREFIX = config.get('contact_form', 'subj_prefix')
CONTACT_FORM_SUBJECT_FMT = CONTACT_FORM_SUBJECT_PREFIX + ' {subject}' if CONTACT_FORM_SUBJECT_PREFIX else '{subject}'
CONTACT_FORM_FROM_EMAIL = config.get('contact_form', 'from_email')

# Smtp
EMAIL_HOST = config.get('smtp', 'host')
EMAIL_HOST_USER = config.get('smtp', 'user')
EMAIL_HOST_PASSWORD = config.get('smtp', 'password')
EMAIL_SUBJECT_PREFIX = '[Website] '
EMAIL_USE_SSL = config.getboolean('smtp', 'ssl')
EMAIL_PORT = config.getint('smtp', 'port')
SERVER_EMAIL = 'finance-django@admin.net.pl'


if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

