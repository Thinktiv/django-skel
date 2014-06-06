# =======================================
#   System Settings - Required by fabfile

PROJECT_NAME = '{{ project_name }}'

# Code repository
# Project Repo
PROJECT_REPO = 'git@github.com:Thinktiv/{{ project_name }}.git'

APP_NAME = 'dj'

# SERVER SETTINGS
WEB_ROOT = '/web/dj'
PROJECT_ROOT = '/web/dj/{{ project_name }}'
CONF_ROOT = '/web/dj/{{ project_name }}/deployment/web-common'  # Point to generated conf files

ENV_NAME = 'dj'
ENV_ROOT = '/web/.virtualenvs'

SUPERVISOR_LOG_DIR = '/var/log/supervisor'
NGINX_LOG_DIR = '/var/log/supervisor/nginx'
CELERYD_LOG_DIR = '/var/log/supervisor/celery'

PGBOUNCER_USERNAME = '{{ project_name }}'
PGBOUNCER_PASSWORD = ''

PROJECT_DOMAIN = '{{ project_name }}.com'
