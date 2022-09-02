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
# import django_heroku
# from decouple import config
# import environ
# env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&qw$#gjx)#=&hti^hwpn*zmmyq8^%0tp0m(u^&&)q)b3f_6-4w'
# SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = str(os.environ.get('DEBUG')) == "1"


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*", "neugott.com", "www.neugott.com",]
# ALLOWED_HOSTS = str(os.environ.get('ALLOWED_HOST')).split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    #authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.facebook',
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
    "q.apps.QConfig",
    # third party apps
    'crispy_forms',
    'ckeditor',
    'rest_framework',

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
# add the service worker location
# start rendering this from the staticfiles dir
PWA_SERVICE_WORKER_PATH = BASE_DIR / 'static/js' / 'serviceworker.js'

PWA_APP_NAME = 'NeuGott Lite'
PWA_APP_DESCRIPTION = "NeuGott Lite"
PWA_APP_THEME_COLOR = '#fff'
PWA_APP_BACKGROUND_COLOR = '#fff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/' # change it to / if it gives an error
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/quiz/' #change to /quiz/
PWA_APP_STATUS_BAR_COLOR = '#fff' #'default'
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
X_FRAME_OPTIONS = 'SAMEORIGIN'

CRISPY_TEMPLATE_PACK = "bootstrap4"



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "core.middleware.LoggingMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
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

# DATABASES = {   
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
# }



DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'postgres',
         'USER': 'dbmasteruser',
         'PASSWORD': '?xQ(1JSI]nZG^-4?nXitnv[$Leg]3gLp', 
         'HOST': 'ls-33d64515978a764b1cff2ac8c0e56c45d199c5d7.czzbhfz5hxzc.eu-west-2.rds.amazonaws.com',
         'PORT': '5432',
     }
 }

# DATABASES = {
#     'default' : {},
#     'auth_db':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'auth.db.sqlite3',  
#     },
#     'object_db':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'object.db.sqlite3',  
#     },
# }



# DATABASES = {
#     'default' : {},
#     'primary_db':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         
# 
# 
# 'NAME': BASE_DIR / 'primary.db.sqlite3',  
#     },
#     'replica1_db':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'replica1.db.sqlite3',  
#     },
#      'replica2_db':{
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'replica2.db.sqlite3',  
#     },
# }


# DATABASE_ROUTERS = ['routers.db_routers.AuthRouter','routers.db_routers.ObjectRouter']
# DATABASE_ROUTERS = ['routers.db_routers.ReplicaRouter']



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
    BASE_DIR  / 'quiz' / 'static',
    BASE_DIR / 'question' / 'static',
    BASE_DIR / 'core'/ 'static',
    BASE_DIR /'ads' / 'static',
    BASE_DIR /'q' / 'static',
    BASE_DIR /'leaderboard' / 'static',

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
# django_heroku.settings(locals())


#SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'olumidejonathan@zohomail.com'
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












# ckeditor configurations

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True
AWS_QUERYSTRING_AUTH = False
CKEDITOR_ALLOW_NONIMAGE_FILES = False # change this settings to True if you want other file formats other than image only
X_FRAME_OPTIONS = 'SAMEORIGIN'




CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            # you can use all these settings in your ads section.
            # {'name': 'document', 'items': ["""'Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-',""" 'Templates', 'Source', 'Preview']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo']},
            # {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            # {'name': 'forms',
            #  'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                    #    'HiddenField']},
            # '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Underline', 'Italic', """'Strike',""", 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            # '/',
            # {'name': 'paragraph',
            #  'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                    #    'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                    #    'Language']},
            # '/',

            # {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': [ 'Table', """ 'Image', 'Flash', 'Smiley', 'SpecialChar', 'HorizontalRule', 'PageBreak', 'Iframe'"""]},
            # '/',
            # {'name': 'styles', 'items': ['Styles',""" 'Format',""" 'Font', 'FontSize']},
            # {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            # {'name': 'tools', 'items': ['Maximize', """'ShowBlocks'"""]},
            # {'name': 'about', 'items': ['About']},
            # '/',  # put this to force next toolbar on new line
            # {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                # 'Preview',
                # 'Maximize',

            # ]},
        ],
        # 'toolbar': 'Basic',  # put selected toolbar config here

        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': '20vh',
        'width': '98%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        'mathJaxLib': 'https://cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            # 'uploadimage', # the upload image feature
            # your extra plugins here
            # 'div',
            # 'autolink',
            # 'autoembed',
            # 'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

