import os, sys
from logging import Handler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justin Quick', 'justquick@gmail.com'),
)

ENGINE = 'django.db.backends.sqlite3'
NAME = 'test'

DATABASES = {
    'default': {
        'ENGINE': ENGINE, # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': NAME,                      # Or path to database file if using sqlite3.
    }
}

# Django 1.1 compat
DATABASE_ENGINE = ENGINE
DATABASE_NAME = NAME

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wzf0h@r2u%m^_zgj^39qwerqwerwerwerq1asdfasdfasdft%^2!p'

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'sitemapext',
)

SITEMAPS_CONFIG = {
    'DEBUG': True
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}