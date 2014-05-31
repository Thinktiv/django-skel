import logging

from django.conf import settings
from django.utils.importlib import import_module
from celery.app import shared_task


log = logging.getLogger('periodic_tasks')


@shared_task
def clear_expired_sessions():
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        log.error("Session engine '{}' doesn't support clearing expired sessions.\n".format(settings.SESSION_ENGINE))
