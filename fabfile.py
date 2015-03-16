"""

Commands include:
    - fab local setupwizard
        - Creates configuration and connection settings to AWS for first time use.
          Adds the new host to the hostfile for production environment.

     - fab production instance
        - Creates a new EC2 instance form a blank AMI image. Instance will be setup based on your server template.

    - fab production serversetup
        - Runs and configures server software and services i.e. Gunicorn, Supervisor and Nginx.

    - fab production deploy
        - Pulls the latest commit from the master branch locally and zips up a release. deploys files to server,
          collects the static files, syncs the db and restarts the server.

    - fab production update
        - Updates/Installs OS site packages.

    - fab production requirements
        - Runs the pip installs all requirements.txt command

    - fab production static
        - Runs the collectstatic command.

    - fab production sync
        - Runs syncdb or migration tasks against a database.

    - fab production reboot
        - Reboots a EC2 instance.2

    - fab production createsuperuser
        - Creates a new superuser against a database.

"""
import os
import time
import importlib

from fabric.operations import prompt
from fabric.contrib.console import confirm
from fabric.api import task, settings, sudo, execute, env, run, cd, local, put, abort, get, hosts

from aws_fabric.setup.tasks import _Wizard
from aws_fabric.utilities import _run_task, add_to_hosts, get_hosts_list, get_settings
from aws_fabric.ec2.api import _create_instance


def base_environment_settings():
    """
    Common environment settings.
    """
    env.release_stamp = time.strftime('%Y%m%d%H%M%S')
    env.connection_attempts = 5
    env.local_repo = settings['LOCAL_REPO']
    env.server_repo = settings['SERVER_REPO']
    env.user = settings['AWS_USER']
    env.key_filename = settings['AWS_PRIVATE_FILE']
    env.aws_key = settings['AWS_KEY']
    env.aws_secret_key = settings['AWS_SECRET_KEY']
    env.hosts = get_hosts_list(local_path, staging=True)
    env.template = settings['TEMPLATE']
    env.aws_ami = settings['AWS_AMI']
    env.tasks = importlib.import_module("aws_fabric.environments.%s.%s" % (env.template, "tasks"))


def staging():
    base_environment_settings()
    env.environment = 'staging'
    env.branch = "develop"


def production():
    base_environment_settings()
    env.branch = "master"
    env.environment = 'production'
    env.server_type = {
        'web': {
            'image_id': 'ami-0ea61279',
            'instance_type': 't1.micro',
            'security_groups': ['web'],
        },
    }


def setupwizard():
    """
    A Wizard that creates a new AWS environment for deployment.
    """
    # Run setup
    _Wizard().run()


def serversetup():
    """
    Public function that configure and setup server software i.e. Gunicorn, Supervisor and Nginx.
    """
    _server_setup()



def instance():
    """
    Creates an EC2 instance from an AMI and configures it based on setup template.
    """
    # Use Boto to create an EC2 instance.
    env.host_string = _create_instance()

    # Run standard tasks.
    _update_os()
    _run_task(env.tasks.build_essentials, "Building server essentials...", "Finished building essentials")
    _deploy_project()
    _install_requirements()
    if confirm("Do you want to collect static", False):
        _collect_static()
    if confirm("Do you want to run the syncdb / migration command for your data?", False):
        _sync_db()
    _server_setup()
    _restart_services()

    if confirm("Do you want to add this new instance to your hosts.py? (recommended)", True):
        add_to_hosts(env.local_repo + "/aws_fabric/config", env.host_string)


def update():
    """
    Runs command to update OS site packages.
    """
    _update_os()


def deploy():
    """
    Public function that deploys a new release from master to server.
    """
    env.release_stamp = time.strftime('%Y%m%d%H%M%S')
    _deploy_project()
    # Update any environment variables.
    _set_update_environment_vars()
    if confirm("Do you want to update requirements?", False):
        _install_requirements()
    if confirm("Do you want to run the collectstatic command", False):
        _collect_static()
    if confirm("Do you want to run the syncdb / migration command for your data?", False):
        _sync_db()

    _restart_services()


def requirements():
    """
    Public function that pip installs all requirements.txt
    """
    _install_requirements()


def static():
    """
    Public function that runs Django's collect static command.
    """
    _collect_static()


def sync():
    """
    Public function that runs syncdb or migration tasks.
    """
    _sync_db()


def reload():
    """
    Public function that restarts all services i.e. Gunicorn, Supervisor and Nginx.
    """
    _restart_services()


def reboot():
    """
    Public function that reboots an EC2 instance.
    """
    _reboot_instance()


def createsuperuser():
    """
    Punlic function to runs the create_superuser Django command.
    """
    _create_superuser()


def environment_vars():
    """
    Set/Update environment variables.
    """
    _set_update_environment_vars()



"""
Private functions
"""


def _deploy_project():
    """
    Private function that runs the deploy task when called.
    """
    _run_task(env.tasks.deploy_release, "Deploying release...", "Finished deploying release")


def _update_os():
    """
    Private function that updates OS
    """
    _run_task(env.tasks.update_os, "Updating OS...", "Finished updating OS")


def _install_requirements():
    """
    Private function that pip installs all requirements.txt
    """
    _run_task(env.tasks.install_requirements, "Installing requirements...", "Finished installing requirements")


def _collect_static():
    """
    Private function that runs Django's collect static command.
    """
    _run_task(env.tasks.collect_static, "Collecting static files...", "Finished collecting static files")


def _sync_db():
    """
    Private function that runs syncdb or migration tasks.
    """
    _run_task(env.tasks.sync_db, "Migrating data...", "Finished migrating data")


def _restart_services():
    """
    Private function that restarts all services i.e. Gunicorn, Supervisor and Nginx.
    """
    _run_task(env.tasks.restart_services, "Reloading services...", "Finished reloading services")


def _reboot_instance():
    """
    Private function that reboots EC2 instance.
    """
    _run_task(env.tasks.reboot_instance, "Rebooting instance...", "System is in reboot mode.")


def _create_superuser():
    """
    Private function to runs the create_superuser Django command.
    """
    _run_task(env.tasks.create_superuser, "Rebooting instance...", "System is in reboot mode, give it a sec!")


def _server_setup():
    """
    Private function that configure and setup server software i.e. Gunicorn, Supervisor and Nginx.
    """
    _run_task(env.tasks.setup_server, "Setting up server services/software...",
              "Finished setting up server services/software")

def _set_update_environment_vars():
    """
    Private function to set/update the system environment variables.
    """
    _run_task(env.tasks.set_update_env_vars, "Setting/Updating Environment Variables...",
              "Finished Setting/Updating Environment Variable.s")