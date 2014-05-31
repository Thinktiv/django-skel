try:
    from . import dev_local as dev
except ImportError:
    from . import dev

import os
import logging


class Settings (dev.Settings):
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    logging.disable(logging.CRITICAL)

    DEBUG = True

    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    FIXTURE_DIRS = dev.Settings.FIXTURE_DIRS + (os.path.join(dev.Settings.DJANGO_ROOT, 'libs/test-fixtures/'),)

    CELERY_ALWAYS_EAGER = True  # Only to be used for testing purposes
    COMPRESS_ENABLED = False
    MEDIA_ROOT = os.path.join(dev.Settings.DJANGO_ROOT, 'media-test/')

    # Re assigning because debug_toolbar should not be included while testing
    INSTALLED_APPS = dev.Settings.DJANGO_APPS + dev.Settings.THIRD_PARTY_APPS + dev.Settings.LOCAL_APPS

    TESTING = True
