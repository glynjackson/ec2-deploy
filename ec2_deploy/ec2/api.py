import time

import boto
import boto.ec2

from fabric.api import task, settings, sudo, execute, env, run, cd, local, put, abort, get, hosts

from ec2_deploy.connections import AWS
from ec2_deploy.notifications import Notification


def _create_instance(instance_type='web', address=None):
    """
    Creates EC2 Instance using boto.
    """
    # Open connection to AWS
    try:
        connection = AWS(access_key=env.aws_key, secret_key=env.aws_secret_key).connect()
    except Exception:
        Notification("Could not connect to AWS").error()
        abort("Exited!")

    Notification('Spinning up the instance...').info()

    # Create new instance using boto.
    reservation = connection.run_instances(**env.server_type[instance_type])
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


