"""
Customise environment task.py for the type of server.

Environment AWS:
    - Ubuntu Server 14.04 LTS
      Nginx (80)
      Gunicorn (8002)
      Supervisor


Hooks (* run in the functions):
    - update_os *instance, *update
        - Actions to update/install standard OS packages.

    - setup_server *instance
        Actions that configure and setup server software i.e. Gunicorn, Supervisor and Nginx.

    - build_essentials *instance
        - Actions to install/update main packages to support setup i.e. pip, git etc.

    - deploy_release *instance, *deploy
        - Actions to upload local project to live production server.

    - install_requirements *instance, *requirements
        - Action to install requirements.txt.

    - collect_static *deploy, *collect
        - Actions to run Django's collectstatic command.

    - sync_db *deploy, *sync
        - Actions that runs syncdb or migration tasks against a database.

    - restart_services *deploy, *reload
        - Actions to restart all services i.e. Gunicorn, Supervisor and Nginx.

    - reboot_instance *reboot
        - Actions to reboot EC2 instance.

    - create_superuser *createsuperuser
        - Action to run the create_superuser command.


"""


# updates then installs the list of available packages for OS.
update_os = [
    {"action": "sudo", "params": "apt-get --yes update", "message": "Updating"},
    {"action": "sudo", "params": "apt-get --yes upgrade", "message": "Upgrading"},
]
# main server build, install server packages.
build_essentials = [

    {"action": "sudo",
     "params": "add-apt-repository 'deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe'",
     "message": "Adding main repository for 14.04"},
    {"action": "sudo", "params": "apt-get --yes install python-pip python-dev build-essential",
     "message": "Installing Python environment"},
    {"action": "sudo", "params": "apt-get --yes install libmysqlclient-dev"},
    {"action": "sudo", "params": "aptitude install -y libapache2-mod-wsgi"},
    {"action": "sudo", "params": "apt-get --yes install git-core", "message": "Installing Git"},
    {"action": "sudo", "params": "apt-get --yes install libmemcached-dev"},
    {"action": "sudo", "params": "mkdir -p %(server_repo)s"},
    {"action": "sudo", "params": "mkdir %(server_repo)s/releases"},
    {"action": "sudo", "params": "mkdir %(server_repo)s/static"},
    {"action": "sudo", "params": "mkdir %(server_repo)s/logs"},

]

setup_server = [
    {"action": "sudo", "params": "pip install git+https://github.com/benoitc/gunicorn.git",
     "message": "Pip installing WSGI HTTP Server Gunicorn"},
    {"action": "sudo", "params": "cp -fr %(server_repo)s/aws_fabric/environments/%(template)s/wsgi.py %(server_repo)s",
     "message": "Copying WSGI"},
    {"action": "sudo", "params": "apt-get --yes install supervisor", "message": "Setting up supervisor"},
    {"action": "sudo", "params": "apt-get --yes install libevent-dev", "message": "Installing workers"},
    {"action": "sudo", "params": "easy_install greenlet", "message": "Greenlet install"},
    {"action": "sudo", "params": "easy_install gevent", "message": "Gevent install"},

    {"action": "sudo",
     "params": "cp -fr %(server_repo)s/aws_fabric/environments/%(template)s/start_gunicorn.conf /etc/supervisor/conf.d/",
     "message": "Creating a start-up process for Gunicorn"},

    {"action": "sudo", "params": "apt-get --yes install nginx", "message": "Installing nginx"},

    {"action": "sudo",
     "params": "cp -fr %(server_repo)s/aws_fabric/environments/%(template)s/default /etc/nginx/sites-available",
     "message": "Copying Nginx config file to location /etc/nginx/sites-available"},

    {"action": "sudo", "params": "apt-get --yes install libjpeg-dev", "message": "Installing libjpeg-dev"},


]


# Create an archive from the current Git release/master branch and upload.
deploy_release = [
    {"action": "local",
     "params": "cd %(local_repo)s; git archive --format=tar %(branch)s | gzip > %(release_stamp)s.tar.gz;",
     "message": "Archiving project for deployment"},
    {"action": "upload_template",
     "params": {"filename": "%(local_repo)s/%(release_stamp)s.tar.gz", "destination": "%(server_repo)s"},
     "message": "Upload file to a remote host"},
    {"action": "sudo", "params": "cd %(server_repo)s; tar -xzvf %(server_repo)s/%(release_stamp)s.tar.gz;",
     "message": "Unpacking release"},


    {"action": "local", "params": "rm %(local_repo)s/%(release_stamp)s.tar.gz",
     "message": "Doing some housekeeping"},


    {"action": "sudo", "params": "cd %(server_repo)s; rm %(server_repo)s/%(release_stamp)s.tar.gz;",
     "message": "Doing some housekeeping"},
]

install_requirements = [
    {"action": "pip", "params": ["-r %(server_repo)s/requirements.txt"]},
]

collect_static = [
    {"action": "sudo", "params": "python %(server_repo)s/manage.py collectstatic"},
]

sync_db = [
    {"action": "sudo", "params": "python %(server_repo)s/manage.py migrate", "message": "Migrating DB"},
]

reboot_instance = [

]

create_superuser = [

]


# Tasks to restart services Supervisor and Celery.
restart_services = [
    {"action": "sudo", "params": "supervisorctl reread", "message": "Rereading Supervisor"},
    {"action": "sudo", "params": "supervisorctl update", "message": "Updating Supervisor"},
    {"action": "sudo", "params": "supervisorctl restart gunicorn_process",
     "message": "Restarting Supervisor gunicorn_process process"},

]

set_update_env_vars = [
    {"action": "sudo",
     "params": "cp /srv/%(server_repo)s/server_template/%(template)s/vars_%(environment)s.env /srv/%(server_repo)s/.env",
     "message": "Copying environment variables."},
]
















