import os
from fabric.api import run, sudo, env, cd
from socket import *


PRODUCTION = 'prod'
STAGING = 'stag'

DEVELOP = 'develop'
MASTER = 'master'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env.local_settings = os.path.join(BASE_DIR, './fab_conf.py')

def __load_settings__(path):
    if os.path.exists(path):
        execfile(path, globals(), env)
    else:
        raise Exception("No settings file found at %s" % path)

__load_settings__(env.local_settings)

print "========== Environment ==========="
print env
print "=================================="

#========================================
# # Required Env variables
#========================================
# PROJECT_NAME
# PROJECT_REPO
#
# WEB_ROOT
# PROJECT_ROOT
# CONF_ROOT
#
# ENV_NAME
# ENV_ROOT
# NGINX_LOG_DIR
# CELERYD_LOG_DIR
# PGBOUNCER_USERNAME
# PGBOUNCER_PASSWORD

def pre_setup_checks():
    # run('ssh -T git@github.com')

    #    # check db server connection
    # if(not _is_host_up('db-server', '5432')):
    #    print "DB server is not setup correctly, Please set that up and try again."

    return True

def setup():
    """
    Method to setup a new web server - only services if codebase is already setup
    Eg. calls#
    fab -f ./fabric.py --hosts=localhost setup
    """

    if(not pre_setup_checks()):
        print "Error. can not continue"

    sudo('chown ubuntu:ubuntu -R /web/.virtualenvs')

    setup_codebase(MASTER)

    setup_env()

    configure_pgbouncer()

    configure_supervisor(PRODUCTION)


def setup_staging():
    """
    Method to setup a new web server - only services if codebase is already setup
    Eg. calls#
    fab -f ./fabric.py --hosts=localhost setup
    """

    sudo('chown ubuntu:ubuntu -R /web/.virtualenvs')

    setup_codebase(DEVELOP)

    setup_env()

    configure_supervisor(STAGING)


############ Helper Methods ###########################
def _is_host_up(host, port):
    targetIP = gethostbyname(host)
    print 'Starting scan on host ', targetIP

    s = socket(AF_INET, SOCK_STREAM)
    result = s.connect_ex((targetIP, port))

    print 'Port %d: %s' % (port, result)
    if(result == 0) :
        return True
    else:
        return False

    s.close()


def setup_codebase(branch):
    run("mkdir -p %s" % env.WEB_ROOT)
    with cd(env.WEB_ROOT):
        run("git clone %s" % env.PROJECT_REPO)
    with cd(env.PROJECT_ROOT):
        run('git pull origin %s' % branch)  # update from git
        run('git checkout %s' % branch)  # update project code

def setup_env():
    run("mkvirtualenv %s" % env.ENV_NAME)
    with cd(env.PROJECT_ROOT):
        run("workon %s && pip install -r requirements.txt" % env.ENV_NAME)

def configure_pgbouncer():
    # workaround for a bug in pgbouncer scripts
    with cd("/var/run"):
        sudo('mkdir -p postgresql')
        sudo('chown -R postgres:postgres postgresql')
        sudo('chmod 775 postgresql')

    sudo('echo \'"%s" "%s"\' >> /etc/pgbouncer/userlist.txt' % (env.PGBOUNCER_USERNAME, env.PGBOUNCER_PASSWORD))

def configure_supervisor(sys_type):
    sudo("service supervisor stop", pty=False)
    sudo("pkill supervisor", pty=False)  # because socket file doesn't get unlinked for some reason
    sudo('mkdir -p %s' % env.NGINX_LOG_DIR)
    sudo('chown www-data:www-data -R %s' % env.NGINX_LOG_DIR)
    sudo('mkdir -p %s' % env.CELERYD_LOG_DIR)
    sudo('chown www-data:www-data -R %s' % env.CELERYD_LOG_DIR)

    with cd("/etc/"):
        sudo('mv supervisord.conf supervisord.conf.back')
        # update the default conf file
        sudo('ln -s {}/supervisord_{}.conf supervisord.conf'.format(env.CONF_ROOT, sys_type))
        with cd("supervisor/"):
            sudo('mv supervisord.conf supervisord.conf.back')
            # update the default conf file on Debian systems
            sudo('ln -s {}/supervisord_{}.conf supervisord.conf'.format(env.CONF_ROOT, sys_type))


    sudo("service supervisor start", pty=False)

#####################################################
# Web & DB server AMI install methods
#####################################################

def prepare_db():
    """
    Method to setup a new web server - AMI setup
    Eg. calls#
    fab -f ./fabric.py --hosts=localhost prepare_db
    """

    upgrade()

    # Install basic dependencies
    sudo('apt-get -y install build-essential python-software-properties iptables-persistent')

    install_rabbitmq()
    install_postgres_server()

def prepare_web():
    """
    Method to setup a new web server - AMI setup
    Eg. calls#
    fab -f ./fabric.py --hosts=localhost prepare_web
    """

    upgrade()
    fix_lib_jpeg()

    # Install basic dependencies
    sudo(
        'apt-get -y install'
        'build-essential libxml2-dev libxslt-dev python-dev python-software-properties iptables-persistent python-setuptools python-pip libmemcached-dev'
    )


    install_postgres_client()
    install_nginx()

    prepare_directories()

    # Install Uwsgi, Pgbouncer
    sudo('apt-get -y install pgbouncer')
    install_uwsgi()

    install_supervisor()
    install_virtualenv(PRODUCTION)
    install_git()
    install_less()

    print('Git install finished, please add generate (ssh-keygen -t rsa -C "amit.yadav@joshlabs.in") and ssh keys to Git repository.')


def prerare_staging():
#     upgrade()
#     fix_lib_jpeg()
    sudo('apt-get -y update')

    # Install basic dependencies
    sudo(
        'apt-get -y install'
        'build-essential libxml2-dev libxslt-dev python-dev python-software-properties iptables-persistent python-setuptools python-pip libmemcached-dev'
    )

    prepare_directories()

    install_postgres_server()
    sudo('apt-get -y install libpq-dev')
    install_nginx()
    install_uwsgi()

    install_rabbitmq()
    install_supervisor(managed_services=['nginx'])
    install_virtualenv(PRODUCTION)
    install_git()
    install_less()

    print('Git install finished, please add generate (ssh-keygen -t rsa -C "{{ project_name }}_staging@{{ project_name }}.com") and ssh keys to Git repository.')


def upgrade():
    sudo('aptitude -y full-upgrade')
    sudo('apt-get -y update')

def fix_lib_jpeg():
    sudo('apt-get -y install libfreetype6-dev libjpeg62-dev')
    so_files = ['libz.so', 'libfreetype.so', 'libjpeg.so', 'libfreetype.so.6', 'libjpeg.so.62']
    for f in so_files:
        sudo('ln -s /usr/lib/x86_64-linux-gnu/%s /usr/lib/' % f)

def setup_user():
#    sudo useradd -d /home/ubuntu -m ubuntu -s /bin/bash
#    sudo adduser ubuntu sudo
#    sudo echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
#    su - ubuntu
#    mkdir ~/.ssh
#    chmod 700 ~/.ssh
#    vim .ssh/authorized_keys
#    #paste keys
#
#    sudo vim /etc/ssh/sshd_config
#    #PermitRootLogin no
#    #PasswordAuthentication no
#
#    sudo /etc/init.d/ssh restart
    pass

def prepare_directories():
    # Prepare directories
    sudo('mkdir -p /web')
    sudo('chown ubuntu:ubuntu -R /web')

    sudo('mkdir -p /web/.virtualenvs')
    sudo('chown ubuntu:ubuntu -R /web/.virtualenvs')


def install_postgres_client():
    # Install Postgres Client
    sudo('add-apt-repository -y ppa:pitti/postgresql')
    sudo('apt-get -y update ')
    sudo('apt-get -y install postgresql-client libpq-dev')

def install_postgres_server():
    # Install Postgres Server
#     sudo('add-apt-repository -y ppa:pitti/postgresql')  #NOTE: giving 404 error
#     sudo('apt-get -y update')
    sudo('apt-get -y install postgresql')

def install_nginx():
    # Install Nginx
    sudo('add-apt-repository -y ppa:nginx/stable')
    sudo('apt-get -y update ')
    sudo('apt-get -y install nginx')

def install_virtualenv(sys_type):
    # Install virtualenv
    sudo('pip install virtualenv')
    sudo('pip install virtualenvwrapper')

    bash_settings = [
        'export WORKON_HOME=/web/.virtualenvs',
        'export PROJECT_HOME=/web/dj',
        'export DJANGO_SETTINGS_MODULE="{{ project_name }}.settings.{}"'.format(sys_type),
        'source /usr/local/bin/virtualenvwrapper.sh'
    ]

    for line in bash_settings:
        run("echo '%s' >> ~/.bash_profile" % line)

    sudo('chown ubuntu:ubuntu -R /web/.virtualenvs')

def install_supervisor(managed_services=None):
    # Install Supervisor
    sudo('apt-get -y install supervisor')  # install system package first
    sudo('pip install supervisor --upgrade')  # upgrade to latest version
    # Disable all supervisor managed services
    managed_services = managed_services or ['nginx', 'pgbouncer']
    for service in managed_services:
        sudo('service %s stop' % service)
        sudo('update-rc.d -f %s remove' % service)


def install_git():
    sudo('apt-get -y install git-core')
    run('git config --global user.name "{{ project_name }} staging"')
    run('git config --global user.email "{{ project_name }}_staging@{{ project_name }}.com"')

    # run('ssh-keygen -t rsa -C "amit.yadav@joshlabs.in"') #generate key pair


def install_less():
    """
    Setup less for Twitter Bootstrap
    """
    # install node package manager
    sudo('apt-get install npm')

    # Update the node_js via npm
    sudo('npm cache clean -f')
    sudo('npm install -g n')
    sudo('n stable')

    # install less via npm
    sudo('npm install -g less')


def install_rabbitmq():
    # Install rabbitmq for queue management
    sudo('apt-get -y install rabbitmq-server')

def install_uwsgi():
    sudo('pip install uwsgi')
