"""Development settings and globals."""

from . import common


class Settings(common.Settings):

    ########## DATABASE CONFIGURATION

    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'project_dev',  # Or path to database file if using sqlite3.
            'USER': 'postgres',  # Not used with sqlite3.
            'PASSWORD': 'password',  # Not used with sqlite3.
            'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
        }
    }
    ########## END DATABASE CONFIGURATION

    ########## CACHE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'project-default'
        }
    }
    ########## END CACHE CONFIGURATION

    ########### CELERY CONFIGURATION
    # # See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
    # CELERY_ALWAYS_EAGER = True
    #
    # # See: http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions
    # CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    ########### END CELERY CONFIGURATION

    ########### EMAIL CONFIGURATION
    ## See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    #EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ########### END EMAIL CONFIGURATION


    ########## TOOLBAR CONFIGURATION
    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    THIRD_PARTY_APPS = common.Settings.THIRD_PARTY_APPS + (
        'debug_toolbar',
    )

    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    INTERNAL_IPS = ('127.0.0.1',)

    # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
    MIDDLEWARE_CLASSES = common.Settings.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
    ########## END TOOLBAR CONFIGURATION
