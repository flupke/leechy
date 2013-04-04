# Destination host
host = 'leechy@leechy.example.com'

# Backend processes will be run under this user
user = 'leechy'

# Absolute path where leechy will be deployed. Make sure it's empty as leechy
# will put all its mess in here.
deploy_dir = '/home/leechy'

# Postgresql settings
db_name = 'leechy'
db_user = 'leechy'
db_password = 'leechy'

# Leechy URL and port
url = 'leechy.example.com'
port = 80

try:
    from .local import *
except ImportError:
    pass
