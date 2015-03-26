
EC2 Deploy is a convenient deployment tool to facilitate code deployment and other tasks to AWS EC2.

Key Features

* Creates new EC2 instances based on a server template.
* Add environment variables to your Python or Django Project.
* Deploy your git repo to staging and production servers.


Installation Steps
------------------

Your project must have a ``requirements.txt`` file even if you don't have any.

Your project must be using ``Git`` with a ``master`` and ``develop`` branch.
Master is used for release to production where develop is used for you staging server.

1 - Install The EC2 Deploy Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need to ``pip`` install EC2 Deploy within your virtual environment.
To get the latest stable release from PyPi enter the following::

    pip install ec2-deploy

2 - Import Fabric Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~

To make use of the Fabric commands within EC2 Deploy you must import them within your own ``fabfile.py`` file.
EC2 Deploy will automatically install Frabric as a dependency if you don't have it already.
Once you have your ``fabfile.py`` add the following import to the top of the file::

    from ec2_deploy.fab import *

3 - Pick Server Template
~~~~~~~~~~~~~~~~~~~~~~~~

The next task is to pick your server template from the directory ``server-template``
and edit the following files to reflect your own remote setup.

For example the template ``AWS_Ubuntu14_04_LTS`` runs a Nginx, Gunicorn setup for Django.

 * ``default`` - Nginx Site File
 * ``start_gunicorn.conf``
 * ``gunicorn.conf.py``
 * ``wsgi.py`` - Remote server wsgi

You can create your own server template by copying an existing one, then modifying the file ``tasks.py``
as required for your own setup.

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

EC2 Deploy gives you a very useful environment variable file with ``python-dotenv``, which
reads values from .env file and loads them as environment variables.

For your remote server you set these variables in ``vars_production.env`` and ``vars_staging.env`` found within the
server template used. EC2 Deploy will create your server environment variables based on the command used during
deployment or server creation.

For example ``fab staging deploy`` would copy the environment variables from the file ``vars_staging.env`` within
your server template folder as ``.env``.

At a minimum you must set the following environment variable within ``vars_production.env`` and ``vars_staging.env``::

    EC2_DEPLOY_SERVER_REPO="/srv/[APP_FOLDER]"

Replacing ``[APP_FOLDER]`` with the folder where your application is located on the remote server.
You can of course use any the same file to store your own custom variables for both your
staging and production environments.

Running a local version of your application requires you to create your own ``.env`` file with some additional variables.

Example **required** local``.env`` file::

    EC2_DEPLOY_AWS_SECRET_KEY = ''
    EC2_DEPLOY_SERVER_REPO="/srv/[APP_FOLDER]"
    EC2_DEPLOY_AWS_KEY = ''
    EC2_DEPLOY_AWS_PRIVATE_FILE = ''
    EC2_DEPLOY_LOCAL_REPO = ''
    EC2_DEPLOY_TEMPLATE = 'ubuntu14custom'
    EC2_DEPLOY_AWS_USER = 'ubuntu'

List of Fabric Commands
-----------------------

There are a number of convenient Fabric scrips available to facilitate code deployment and other server tasks on AWS EC2.

**Note:** Local environment must be configured correctly to run Fabric tasks *(see environment variables above)*.

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