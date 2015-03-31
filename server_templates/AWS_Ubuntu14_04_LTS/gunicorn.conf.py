import os
import dotenv


def get_workers_count_based_on_cpu_count():
    """
    Returns the number of workers based available virtual or physical CPUs on this system.
    """
    # Python 2.6+
    try:
        import multiprocessing

        return multiprocessing.cpu_count() * 2 + 1
    except (ImportError, NotImplementedError):
        pass
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))
        if res > 0:
            return res * 2 + 1
    except (AttributeError, ValueError):
        pass

    raise Exception('Can not determine number of CPUs on this system')


dotenv.load_dotenv('.env')

bind = "127.0.0.1:8002"
workers = get_workers_count_based_on_cpu_count()
worker_class = 'gevent'

max_requests = 1000
timeout = 302
keep_alive = 2

preload = True

# Logging
errorlog = '{}/logs/error.log'.format(os.environ['EC2_DEPLOY_SERVER_REPO'])
# A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'