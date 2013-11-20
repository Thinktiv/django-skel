import logging
from django.conf import settings
from django.utils.importlib import import_module
from celery.schedules import crontab
from celery.task import periodic_task

log = logging.getLogger('periodic_tasks')


@periodic_task(run_every=crontab(minute=0, hour=6))
def clear_expired_sessions():
    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        log.error("Session engine '{}' doesn't support clearing expired sessions.\n".format(settings.SESSION_ENGINE))
