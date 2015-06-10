from . import prod
from os import environ

# Parse database configuration from $DATABASE_URL


class Settings(prod.Settings):

    ########## CELERY CONFIGURATION
    # See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
    # This might create Error loop if Connection Error occurs while establishing connection to ampq
    # Another solution could be to use a backend other than ampq
    # CELERY_RESULT_BACKEND = 'amqp'

    CELERY_ALWAYS_EAGER = False
    ########## END CELERY CONFIGURATION

    ########## ALLOWED HOSTS CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['.herokuapp.com']
    ########## END ALLOWED HOST CONFIGURATION

    ######## SENTRY SETTINGS #######################################
    RAVEN_CONFIG = {
        'dsn': environ.get('SENTRY_DSN'),
    }
    ########## END SENTRY SETTINGS #################################
