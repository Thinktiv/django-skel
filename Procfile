web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
scheduler: python manage.py celery worker -B --maxtasksperchild=1000 -n worker1 -c 2
