"""
Django settings for sampleapp project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6vc%#!x-2s(a+i#w%vn+2am0_ug8=+sq8%k%-j8v*%oe(@v01$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # 'suit',

    'jet',
    'jet.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'assistenza',
    'crispy_forms',
    'gare',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'biomedicalservice.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'),
                  os.path.join(BASE_DIR, 'assistenza/templates'),
                  os.path.join(BASE_DIR, 'main/templates'),
                  os.path.join(BASE_DIR, 'AdminLTE'),


        ],
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

WSGI_APPLICATION = 'biomedicalservice.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'it'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# SUIT_CONFIG = {
#     'ADMIN_NAME': 'Biomedical Service',
#
#
#     'HEADER_DATE_FORMAT': 'l, j. F Y',
#     'HEADER_TIME_FORMAT': 'H:i',
#
#     # forms
#     'SHOW_REQUIRED_ASTERISK' : True,  # Default True
#     'CONFIRM_UNSAVED_CHANGES': True, # Default True
#
#     # menu
#     'SEARCH_URL': '/admin/auth/user/',
#     'MENU_ICONS': {
#        'sites': 'icon-leaf',
#        'auth': 'icon-lock',
#     },
#     'MENU_OPEN_FIRST_CHILD': True, # Default True
#     'MENU_EXCLUDE': ('auth.group',),
#
#
#     # misc
#     'LIST_PER_PAGE': 15
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

LOGIN_REDIRECT_URL = "/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media-serve')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'deploy')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

JET_DEFAULT_THEME = 'default'

JET_SIDE_MENU_COMPACT = True

JET_CHANGE_FORM_SIBLING_LINKS = True

JET_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'


JET_SIDE_MENU_ITEMS = [  # A list of application or custom item dicts
    {'label': ('Rubrica'), 'app_label': 'main','items': [
        {'name': 'Clienti', 'label': ('Cliente'), 'url': '/admin/main/cliente/',},
        {'name': 'Fornitori', 'label': ('Fornitore'), 'url': '/admin/main/fornitore/',},
    ]},
        {'label': ('Gestione'), 'app_label': 'main', 'items': [
        {'name': 'Acquisti', 'label': ('Acquisti'), 'url': '/admin/main/acquisti/',},
        {'name': 'Dispositivo', 'label': ('Magazzino'), 'url': '/admin/main/dispositivo/',},
        {'name': 'Fattura', 'label': ('Vendite'), 'url': '/admin/main/fattura/',},
        {'name': 'Installazioni', 'label': ('Installazioni'), 'url': '/admin/main/installazioni/',},

    ]},

    {'label': ('Assistenza'), 'app_label': 'assistenza', 'items': [
        {'name': 'Verifiche', 'label': ('Verifica'), 'url': '/admin/assistenza/verifica/',},
        {'name': 'Riparazioni', 'label': ('Riparazione'), 'url': '/admin/assistenza/riparazione/',},
        {'name': 'Prodotti', 'label': ('Dispositivi'), 'url': '/admin/assistenza/prodotti/',},

    ]},

    {'label': ('Bandi pubblici'), 'app_label': 'gare', 'items': [
        {'name': 'GaraPubblica', 'label': ('Gare'), 'url': '/admin/gare/garapubblica/',},
        { 'label': ('MEPA'), 'url': 'https://www.mepa.it/',},

    ]},

]
