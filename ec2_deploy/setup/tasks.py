import os
import pickle

from fabric.operations import prompt
from fabric.contrib.console import confirm
from fabric.contrib.files import upload_template, exists
from fabric.api import task, settings, sudo, execute, env, run, cd, local, put, abort, get

from aws_fabric.connections import AWS
from aws_fabric.notifications import Notification


class _Wizard(object):
    """
    Public Wizard that helps to configure a new AWS environment config.
    """

    def __init__(self):
        self.environment = Environment()


    def run(self):
        """
        A Wizard that creates and configures a new AWS environment for AWS.y
        """
        Notification(
            'This wizard creates a new AWS environment that can be used in deployment of your project to AWS.').info()
        template_choices = self._get_templates()
        value = prompt('Enter the number that corresponds to the server template you would like to use:',
                       validate=int, default=0)
        self.environment.template = template_choices[int(value)]


        self.environment.local_repo = prompt("What is the full path locally to your project?",
                                             default="/Users/user/Documents/workspace/project_folder")


        self.environment.server_repo = prompt("What will be your server directory for this project?",
                                             default="/srv/project_folder")



        self.environment.aws_user = prompt("What is your EC2 login user:", default="ubuntu")

        self.environment.aws_key = prompt("What is your AWS public key:")
        self.environment.aws_secret_key = prompt("What is your AWS secret key:")

        if confirm("Test AWS connection before continuing?", True):
            Notification('Testing connection').info()
            AWS(access_key=self.environment.aws_key, secret_key=self.environment.aws_secret_key).connect()

        self._set_private_file()
        self._check_private_file_exists()


        # Write the configuration file
        self._write_congif()


    def _write_congif(self):
        """
        Writes the configuration file.
        """
        location = 'aws_fabric/config/settings.py'
        Notification('Attempting to write configuration file %s...' % location).info()
        try:
            with open(location, 'wb') as handle:
                for k, i in self.environment.environment_values.iteritems():
                    handle.write("{} = '{}' \n".format(k.upper(), i))
            Notification('Successful!').success()
        except Exception, e:
            Notification('Error could not write configuration file. %s ' % str(e)).error()


    def _get_templates(self):
        """
        Lists out server templates inside folder aws_fabric/setup/templates and returns dictionary of the folder names.
        """
        template_choices = {}
        templates = os.walk('aws_fabric/environments').next()[1]
        Notification(
            'Found %s server templates that could be used in creating a new instance. These templates contain ' % len(
                templates)).info()
        for index, template in enumerate(templates):
            template_choices[index] = template
            Notification("%s = %s" % (index, template)).info()

        return template_choices

    def _set_private_file(self):
        self.environment.aws_private_file = prompt("Where is your private key file located?",
                                               default="/Users/user/Documents/EC2Keys/project.pem")

    def _check_private_file_exists(self):
        if not os.path.exists(self.environment.aws_private_file):
            Notification('Cannot find path %s please try again...' % self.environment.aws_private_file).error()
            self._set_private_file()
            self._check_private_file_exists()


class Environment(object):
    environment_values = None

    def __init__(self):
        self.environment_values = {}

    def __setattr__(self, key, value):
        if self.environment_values is None:
            # set config directly
            super(Environment, self).__setattr__(key, value)
            return
        self.environment_values[key] = value

    def __getattr__(self, key):
        try:
            return self.environment_values[key]
        except KeyError:
            raise AttributeError(key)






