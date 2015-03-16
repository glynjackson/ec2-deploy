import time

import boto
import boto.ec2

from fabric.api import task, settings, sudo, execute, env, run, cd, local, put, abort, get, hosts
from fabric.operations import prompt

from ec2_deploy.connections import AWS
from ec2_deploy.notifications import Notification


def _create_instance(instance_type='web', address=None):
    """
    Creates a new EC2 Instance using Boto.
    """
    # Open connection to AWS
    try:
        connection = AWS(access_key=env.aws_key, secret_key=env.aws_secret_key).connect()
    except Exception:
        Notification("Could not connect to AWS").error()
        abort("Exited!")

    aws_ami = prompt("Hit enter to use the default Ubuntu AMI or enter one:", default="ami-234ecc54")
    aws_security_groups = prompt("Which security group should this new instance belong to?", default="web")
    aws_instance_type = prompt("What instance type do you want to create? ", default="m3.medium")

    BUILD_SERVER = {
        'image_id': aws_ami,
        'instance_type': aws_instance_type,
        'security_groups': [aws_security_groups],
    }

    Notification('Spinning up the instance...').info()

    # Create new instance using boto.
    reservation = connection.run_instances(**BUILD_SERVER)
    instance = reservation.instances[0]
    time.sleep(5)
    while instance.state != 'running':
        time.sleep(5)
        instance.update()
        Notification('-Instance state: %s' % instance.state).info()

    Notification('Instance %s was created successfully' % instance.id).success()
    # A new instance take a little while to allow connections so sleep for x seconds.
    sleep_for = 10
    Notification('Sleeping for %s seconds before attempting to connect...' % sleep_for).info()
    time.sleep(sleep_for)

    return instance.public_dns_name


