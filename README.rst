Pick Environment
================




Local Environment Setup
=======================

When the codebase is deployed using Fabric, the environment is automatically detected based on the server type staging/production.
However, running a local version of the API requires you to set these environment variables yourself and other configuration/settings data.

When you run any fab command the package will look for a file called ``.env`` in the root directory
(in the same folder as ``manage.py``).

If you required different settings you don't have to set a ``.env`` file.
Because settings use standard environment variables you can either ``export var=xyz`` in shell or create a
``.ssh`` script for each environment yourself i.e.``source yourvars.sh``

**Don't commit your ``.env`` file to GitHub!**

Example ``.env`` settings::

    EC2_DEPLOY_AWS_SECRET_KEY = ''
    EC2_DEPLOY_SERVER_REPO = ''
    EC2_DEPLOY_AWS_KEY = ''
    EC2_DEPLOY_AWS_PRIVATE_FILE = ''
    EC2_DEPLOY_LOCAL_REPO = ''
    EC2_DEPLOY_TEMPLATE = 'ubuntu14custom'
    EC2_DEPLOY_AWS_USER = 'ubuntu'


List of Fabric Commands
=======================

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