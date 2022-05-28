"""
Django settings for tothex project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import django_heroku
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&qw$#gjx)#=&hti^hwpn*zmmyq8^%0tp0m(u^&&)q)b3f_6-4w'
# SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = config('DEBUG', cast=bool, default=True)
ALLOWED_HOSTS = [ "127.0.0.1", "localhost", "0.0.0.0", "https://tothexdemo.herokuapp.com"] 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
    # add twitter and linkedIn
    'django_social_share',
    # the main site apps
    "ads.apps.AdsConfig",
    "category.apps.CategoryConfig",
    "core.apps.CoreConfig",
    "leaderboard.apps.LeaderboardConfig",
    "personalProfile.apps.PersonalprofileConfig",
    "question.apps.QuestionConfig",
    "quiz.apps.QuizConfig",

    # third party apps
    'crispy_forms',


    #progressive web app
    'pwa',
    #  "debug_toolbar",
]





# INTERNAL_IPS = [
#     # ...
#     "127.0.0.1",
#     # ...
# ]






# PROGRESSIVE WEB APP
PWA_SERVICE_WORKER_PATH = BASE_DIR / 'static/js' / 'serviceworker.js'

PWA_APP_NAME = 'ToTheX Lite'
PWA_APP_DESCRIPTION = "ToTheX Lite"
PWA_APP_THEME_COLOR = '#ffffff'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/' # change it to / if it gives an error
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/' #change to /quiz/
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
	{
		'src': 'static/images/tothex_160.png',
		'sizes': '160x160'
	}
]
PWA_APP_ICONS_APPLE = [
	{
		'src': 'static/images/tothex_160.png',
		'sizes': '160x160'
	}
]
PWA_APP_SPLASH_SCREEN = [
	{
		'src': 'static/images/tothex_192.png',
		'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
	}
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
PWA_DEBUG_MODE = False

# crispy forms

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap4"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    "debug_toolbar.middleware.DebugToolbarMiddleware",
]



ROOT_URLCONF = 'tothex.urls'

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
                'django.template.context_processors.request',

            ],
        },
    },
]

WSGI_APPLICATION = 'tothex.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/' 
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'quiz' / 'static',
    BASE_DIR / 'question' / 'static',
    BASE_DIR / 'core' / 'static',
    BASE_DIR / 'ads' / 'static',
]

# media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# login credentials
LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = 'account_login'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
"""
Change this settings later
"""
ACCOUNT_EMAIL_REQUIRED = False # change this to true

SOCIALACCOUNT_QUERY_EMAIL = True # change this to true

ACCOUNT_SESSION_REMEMBER = True
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'






# django hosting configuration
django_heroku.settings(locals())


#SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'olumidejonathan10@gmail.com'
EMAIL_HOST_PASSWORD = 'triumphant'

# SOCIAL AUTHENTICATION_BACKENDS

# 
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        # 'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    }
}


# validating the views before any transaction



# setting the session expiry date

# SESSION_COOKIE_AGE = 60 * 60 # 60 minutes


# celery

CELERY_BEAT_SCHEDULE = {
    "scheduled_tasks" :{
        'task' : 'core.tasks.add',
        'schedule' : 10.0,
        'args' : (10,10),
    },
    "dailyStreakUpdate" : {
        'task' : 'core.tasks.DailyStreakUpdate',
        'schedule' : 10.0, #crontab(minute=0, hour=0),   declare crontab later
    }
}





# celery tasks
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
