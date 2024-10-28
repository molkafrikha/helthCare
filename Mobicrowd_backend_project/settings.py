"""
Django settings for Mobicrowd_backend_project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fv48ny8t8(bcwp3)lvzx&11e*!$_o&mb8(_ufo-%0o%j^&(0i1'  # Change this in production!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Change to False in production!

ALLOWED_HOSTS = ['*']  # Change this for production use

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Added sites framework
    'corsheaders',  # Add corsheaders
    'rest_framework',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'mobicrowd',
    'storages',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'Mobicrowd_backend_project.urls'

# Template Configuration
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
            ],
        },
    },
]

# WSGI Application
WSGI_APPLICATION = 'Mobicrowd_backend_project.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mindcare',  # Change this to your actual database name
        'USER': 'root',      # Change to your database user
        'PASSWORD': '',      # Add your database password
        'HOST': 'localhost',
        'PORT': 3306,
        'OPTIONS': {
            'init_command': 'SET sql_mode="STRICT_ALL_TABLES"',  # Enable strict mode
        },
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'contact@hackhpc.com'
EMAIL_HOST_PASSWORD = 'zkh-7whT?mZL*7G'  # Change this to your actual email password

# Authentication Settings
AUTH_USER_MODEL = 'mobicrowd.User'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

# Base URLs
BASE_URL = 'http://localhost:8000'
FRONTEND_URL = 'http://localhost:4200/sign-in'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = "AKIA23PIJ25VTSP6UA4B"  # Change this to your actual AWS Access Key ID
AWS_SECRET_ACCESS_KEY = "+AymctHUB5pG7HM/R+OVxv9rVVO+z9D/WbrtlCWa"  # Change this to your actual AWS Secret Access Key
AWS_REGION = 'us-east-1'
AWS_STORAGE_BUCKET_NAME = 'mobicrowd'
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'multimedia'

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the message broker
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis as the result backend
CELERY_ACCEPT_CONTENT = ['json']  # Accept JSON serialized tasks
CELERY_TASK_SERIALIZER = 'json'  # Serialize tasks using JSON
CELERY_RESULT_SERIALIZER = 'json'  # Serialize task results using JSON
CELERY_TIMEZONE = 'UTC'  # Set timezone for Celery tasks

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Allow requests from the Angular app
]

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'concise': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'concise',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'mobicrowd': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Added Site ID for django.contrib.sites
SITE_ID = 1  # Set this to the ID of your site
