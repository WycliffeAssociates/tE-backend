bind = ['0.0.0.0:8000']
timeout = 3600
keepalive = 2
workers = 4
worker_class = 'gevent'
worker_connections = 1000
accesslog = 'access.log'
errorlog = 'error.log'
