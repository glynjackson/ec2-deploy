import os
import dotenv
# Load environment vars.
dotenv.load_dotenv('.env')

bind = "127.0.0.1:8002"
workers = 3
worker_class = 'gevent'

max_requests = 1000
timeout = 302
keep_alive = 2

preload = True

# Logging
errorlog = '{}/logs/error.log'.format(os.environ['EC2_DEPLOY_SERVER_REPO'])
# A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'