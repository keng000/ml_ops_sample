
# Nginx Dockerfile

## Environment Variables

### nginx.conf
- WORKER_PROCESSES 
- WORKER_CONNECTIONS 
- KEEPALIVE_TIMEOUT 
- GZIP

### public.conf
- SERVER_PORT
- SERVER_NAME
- LOG_STDOUT
- BASIC_AUTH_FILE

### upstream.conf
- BACKEND_HOST
- BACKEND_MAX_FAILS
- BACKEND_FAIL_TIMEOUT