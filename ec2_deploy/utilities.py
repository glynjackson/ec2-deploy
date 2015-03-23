import time
import os

from fabric.api import *
from fabric.contrib.files import upload_template
from git import Repo

from ec2_deploy.setup.api import has_valid_setup
from ec2_deploy.notifications import Notification


def _run_task(task, start_message, finished_message):
    """
    Tasks a task from tasks.py and runs through the commands on the server
    """
    start = time.time()

    # Check if any hosts exist
    if not has_valid_setup:
        Notification("You don't have a valid setup file. Have you run 'fab setupwizard'?").error()
        abort("Exit")

    Notification(start_message).info()

    # Run the task items
    for item in task:
        try:
            Notification("-" + item['message']).info()
        except KeyError:
            pass
        globals()["_" + item['action']](item['params'])

    Notification("%s in %.2fs" % (finished_message, time.time() - start)).success()


def _sudo(params):
    """
    Run command as root.
    """
    command = _render(params)
    sudo(command)


def _local(params):
    """
    Run command on local machine.
    """
    command = _render(params)
    local(command)


def _pip(params):
    """
    Run pip install command.
    """
    for item in params:
        command = _render(item)
        _sudo("pip install %s" % command)


def _upload_template(params):
    """
    Run command to render and upload a template text file to a remote host.
    """

    upload_template(filename=_render(params['filename']),
                    destination=_render(params['destination']), use_sudo=True)


def _render(template, context=env):
    """
    Does variable replacement %(variable)s
    """
    return template % context


def add_to_hosts(path, instance):
    """
    Takes an instance ID and appends it to a list config/hosts.py
    """
    list_string = get_hosts_list(path)
    list_string.append(instance)
    with open(path + '/hosts.py', 'w') as f:
        f.write(str(list_string))


def get_hosts_list(path, staging=False):
    """
    Reads the hosts.py file and returns the list.
    """
    if staging:
        filepath = path + '/hosts_staging.py'
    else:
        filepath = path + '/hosts.py'

    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            list_string = eval(f.readline())
    else:
        list_string = []

    return list_string


def run_sanity_checks(env):





    Notification("Running sanity checks...").info()

    # Check for git branches master and develop.
    repo = Repo(env.local_repo)
    if repo.bare:
        Notification("No 'git' repo setup.").error_exit()

    print(repo.branches)

    # Check for requirements.text.
    if not os.path.isfile(os.path.expanduser("{}/requirements.txt".format(env.local_repo))):
        Notification("Your local repo does not appear to have a 'requirements.txt'. Please create one in your root.").error_exit()

    # Check for environment vars.
    for var_file in ['vars_production.env', 'vars_staging.env']:

        if not os.path.isfile(
                os.path.expanduser("{}/server_templates/{}/{}".format(env.local_repo, env.template, var_file))):
            Notification("Cannot find environments variable file in server template.").error_exit()

        d = {}
        with open("{}/server_templates/{}/{}".format(env.local_repo, env.template, var_file)) as f:
            for line in f:
                (key, val) = line.split("=")
                d[key] = val
        if len(d) is 0:
            Notification("You have not set any environments variables for {} ".format(var_file)).error_exit()

        if not "EC2_DEPLOY_SERVER_REPO" in d:
            Notification("Please set 'EC2_DEPLOY_SERVER_REPO' in {} ".format(var_file)).error_exit()

        Notification("Passed all checks").success()





























