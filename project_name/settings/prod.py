"""Production settings and globals."""


# from S3 import CallingFormat

from . import stag


class Settings(stag.Settings):
    MIDDLEWARE_CLASSES = ('sslify.middleware.SSLifyMiddleware',) + stag.Settings.MIDDLEWARE_CLASSES

    ########## DATABASE CONFIGURATION
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '{{ project_name }}_prod',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '6432',
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

    ########## ALLOWED HOSTS CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['{{ project_name }}.com']
    ########## END ALLOWED HOST CONFIGURATION

    ########## HTTPS CONFIGURATION
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    # Heroku uses this : https://devcenter.heroku.com/articles/http-routing#heroku-headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    ########## ENDS HTTPS CONFIGURATION

    ########## SENTRY
    RAVEN_CONFIG = {
        'dsn': '',
    }
    ########## END SENTRY

    ########## MICS
    # Robots.txt
    ALLOW_SEARCH_ENGINE_INDEXING = True

    # Disable static urls
    EXPOSE_STATIC_URLS = False
    ########## END MISC
