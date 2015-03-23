Installation Steps
------------------

Your project must have a ``requirements.txt`` file even if you don't have any.
Your project must be using ``Git`` with a ``master`` and ``develop`` branch.

### 1 - Install Package ###

To get the latest stable release from PyPi::

    pip install ec2-deploy

### 2 - Import Fabric Commands ###

Create a file in your root directory called  ``fabfile.py' and add the following to the top of the file::

    from ec2_deploy.fab import *

### 3 - Pick Server Template ###

Pick your server template from the directory ``server-template``, and edit the following files to reflect your own setup.

 * Default
 * etc etc


### Local Environment Setup ###

When the codebase is deployed using Fabric, which environment variables your server should set
is automatically detected based on the command staging/production. Either ``vars_production.env`` or ``vars_staging.env`` will
be deployed.

However, running a local version requires you to create some extra environment variables that are used for deployment
configuration/settings data in a file called ``.env``.


Extra settings needed in your ``.env`` file::

    EC2_DEPLOY_AWS_SECRET_KEY = ''
    EC2_DEPLOY_SERVER_REPO = ''
    EC2_DEPLOY_AWS_KEY = ''
    EC2_DEPLOY_AWS_PRIVATE_FILE = ''
    EC2_DEPLOY_LOCAL_REPO = ''
    EC2_DEPLOY_TEMPLATE = 'ubuntu14custom'
    EC2_DEPLOY_AWS_USER = 'ubuntu'


List of Fabric Commands
-----------------------

There are a number of convenient Fabric scrips available to facilitate code deployment and other server tasks on AWS EC2.

**Note:** Local environment must be configured correctly to run Fabric tasks *(see local environment setup)*.

* ``fab staging/production instance`` - Creates an EC2 instance from an AMI and configures it based on template.
    * Creates new EC2 instance.
    * Updates OS.
    * Builds essential packages.
    * Deploy Master branch.
    * Installs requirements.
    * Server Setup, Gunicorn, Nginx and ports.
    * Celery Setup.
    * Restarts all services.

* ``fab staging/production deploy`` - Deploys API codebase.
    * Deploy form master(staging)/release branch. Creates a release zip.
    * Updates environment variables.
    * Restarts all services.

* ``fab staging/production celery_setup`` - Updates **Supervisor** and **Celery** processes from ``celery.conf``
    * Deploy form Master branch.
    * Updates each Celery worker start process.
    * Restarts Supervisor and Celery worker on the server.

* ``fab staging/production environment_vars`` - Sets or Updates system environment variables.
* ``fab staging/production reload`` - Restarts services.
* ``fab staging/production update`` - Update OS site packages.
* ``fab staging/production requirements`` - Runs ``pip install`` requirements.txt.
* ``fab staging/production serversetup`` - Runs all the build server tasks.
* ``fab staging/production create_swap`` - Creates Swap Memory