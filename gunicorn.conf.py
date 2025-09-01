# Configuración de Gunicorn para Nexa WhatsApp Bot
import multiprocessing

# Configuración del servidor
bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Proceso
preload_app = True
daemon = False
pidfile = "gunicorn.pid"

# Seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
