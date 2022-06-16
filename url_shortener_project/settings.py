"""
Django settings for url_shortener_project project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

from .setup import create_dirs, get_static_dirs, get_template_dirs

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

if DEBUG is True:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

    # CSRF
    CSRF_COOKIE_AGE = 8640000
    CSRF_COOKIE_SECURE = False

    # Data/File Upload
    DATA_UPLOAD_MAX_MEMORY_SIZE = 200000000
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
    FILE_UPLOAD_MAX_MEMORY_SIZE = 200000000

    # Security
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = None
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False

else:
    ALLOWED_HOSTS = ['webhost1.pythonanywhere.com']

    # CSRF
    CSRF_COOKIE_AGE = 86400
    CSRF_COOKIE_SECURE = True

    # Data/File Upload
    DATA_UPLOAD_MAX_MEMORY_SIZE = 200000
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10
    FILE_UPLOAD_MAX_MEMORY_SIZE = 200000

    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Application definition
USER_APPS = [
    'shortener_app'
]

INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                 ] + USER_APPS

# Create necessary directories
create_dirs(BASE_DIR, USER_APPS)

MIDDLEWARE = [
    # added middleware
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'url_shortener_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'csp.context_processors.nonce',
            ],
        },
    },
]
TEMPLATES_DIR = get_template_dirs(USER_APPS)

WSGI_APPLICATION = 'url_shortener_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database' / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = get_static_dirs(USER_APPS)

# Media files (Uploaded files)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Content Security Policy (https://django-csp.readthedocs.io/en/latest/configuration.html)
CSP_INCLUDE_NONCE_IN = ['default-src', 'script-src', 'style-src']

CSP_DEFAULT_SRC = ["'self'", ]
CSP_SCRIPT_SRC = ["'self'", 'https://cdn.jsdelivr.net/', ]
CSP_STYLE_SRC = ["'self'", "https://fonts.googleapis.com/", ]
CSP_IMG_SRC = ["'self'", ]
CSP_PREFETCH_SRC = ["'self'", 'https://cdn.jsdelivr.net/', ]
CSP_FONT_SRC = ["'self'", "https://fonts.gstatic.com/", ]
