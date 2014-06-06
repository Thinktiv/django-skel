import os

from django.conf import settings

from celery import Celery

from {{ project_name }}.libs.commons.utils import get_default_django_settings_module


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', get_default_django_settings_module())
os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')


from configurations import importer
importer.install()


app = Celery('{{ project_name }}')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, 'tasks')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, 'periodic_tasks')
