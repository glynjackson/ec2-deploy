
import time
from boto import ec2
from fabric.api import  settings



import config as config
from notifications import Notification


class AWS(object):

    def __init__(self, access_key=None, secret_key=None):

        self.aws_connection = None
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = ec2.get_region('eu-west-1')

    def connect(self):
        """
        Establishes a connection to AWS.
        """
        Notification('Attempting to establish a connection to AWS').info()
        self.ec2conn = ec2.connection.EC2Connection(self.access_key,
                                                    self.secret_key, region=self.region)

        Notification('Successfully connected').success()

        return self.ec2conn






class EC2Conn:
    def __init__(self):
        self.ec2conn = None
        self.access_key = config.AWS_API_KEY
        self.secret_key = config.AWS_SECRET_KEY
        self.file_key = config.LOCAL_AWS_KEY_FILE
        self.user_name = config.AWS_USER_NAME

    def connect(self):
        Notification('Connecting to the AWS instance').info()
        region = ec2.get_region('eu-west-1')
        self.ec2conn = ec2.connection.EC2Connection(self.access_key,
                                                    self.secret_key, region=region)
        Notification('Successfully connected').success()

    def get_instances(self):
        return self.ec2conn.get_all_instances()



    def open_ec2_connection(self, instance_dns=None):

        if not instance_dns:
            Notification('No DNS information was specified').error()

        Notification('Opening connection to %s' % instance_dns).warning()
        return self._ec2_connection(instance_dns=instance_dns)

    def _ec2_connection(self, instance_dns=None):
        return settings(host_string=instance_dns, key_filename=self.file_key,
                        user=self.user_name, connection_attempts=15)
