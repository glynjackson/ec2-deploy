bind = "127.0.0.1:8002"
workers = 3
worker_class = 'gevent'

max_requests = 1000
timeout = 302
keep_alive = 2

preload = True

# Logging
errorlog = '/srv/DOMAIN/logs/error.log'
# A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'