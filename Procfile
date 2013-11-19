web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
scheduler: python manage.py celery worker -B --maxtasksperchild=1000
worker: python manage.py celery worker --maxtasksperchild=1000
