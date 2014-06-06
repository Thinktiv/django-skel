from . import common


class Settings(common.Settings):
    ########## DEBUG CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = False
    ########## END DEBUG CONFIGURATION

    ########## EMAIL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    EMAIL_HOST = 'smtp.sendgrid.net'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
    EMAIL_HOST_PASSWORD = ''

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
    EMAIL_HOST_USER = ''

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    EMAIL_PORT = '587'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
#     EMAIL_SUBJECT_PREFIX = '[{0}] '.format(common.Settings.SITE_NAME)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
    EMAIL_USE_TLS = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = property(lambda self: self.EMAIL_HOST_USER)
    ########## END EMAIL CONFIGURATION

    ########## DATABASE CONFIGURATION
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '{{ project_name }}_prod',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ########## END DATABASE CONFIGURATION

    ########## CACHE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'BINARY': True,
            'LOCATION': 'localhost:11211',
        }
    }
    ########## END CACHE CONFIGURATION

    ########## CELERY CONFIGURATION
    # See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
    BROKER_TRANSPORT = 'amqplib'

    # Set this number to the amount of allowed concurrent connections on your AMQP
    # provider, divided by the amount of active workers you have.
    #
    # For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
    # they allow 3 concurrent connections. So if you run a single worker, you'd
    # want this number to be 3. If you had 3 workers running, you'd lower this
    # number to 1, since 3 workers each maintaining one open connection = 3
    # connections total.
    #
    # See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
    BROKER_POOL_LIMIT = 1

    # See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
    BROKER_CONNECTION_MAX_RETRIES = 0

    # See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'

    # See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
    # This might create Error loop if Connection Error occurs while establishing connection to ampq
    # Another solution could be to use a backend other than ampq
    # CELERY_RESULT_BACKEND = 'amqp'

    CELERY_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ########## END CELERY CONFIGURATION

    ########## APPS CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    THIRD_PARTY_APPS = common.Settings.THIRD_PARTY_APPS + (
        'storages',
        'raven.contrib.django.raven_compat',  # Sentry
        'djcelery_email',
        'clear_cache',
    )
    ########## END APPS CONFIGURATION

    ########## STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    STATICFILES_STORAGE = 'libs.s3.HerokuStaticS3BotoStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    # AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = ''
    AWS_STATIC_STORAGE_BUCKET_NAME = ''
    AWS_AUTO_CREATE_BUCKET = False
    AWS_QUERYSTRING_AUTH = False

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIRY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY,
            AWS_EXPIRY)
    }

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = 'https://s3.amazonaws.com/{0}/'.format(AWS_STATIC_STORAGE_BUCKET_NAME)

    MEDIA_URL = 'https://s3.amazonaws.com/{0}/'.format(AWS_STORAGE_BUCKET_NAME)
    ########## END STORAGE CONFIGURATION

    ########## COMPRESSION CONFIGURATION
    # See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
    COMPRESS_ENABLED = True

    # See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
    COMPRESS_OFFLINE = False
    ########## END COMPRESSION CONFIGURATION

    ########## ALLOWED HOSTS CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['*']
    ########## END ALLOWED HOST CONFIGURATION
