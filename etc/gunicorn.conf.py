import os
import os.path as op
import sys
import site


ROOT_DIR = op.abspath(op.join(op.dirname(__file__), ".."))


def setup_venv(vepath):
    # Remember original sys.path.
    prev_sys_path = list(sys.path) 
    # Add venv"s site-packages directory.
    site.addsitedir(vepath)
    # Reorder sys.path so new directories are at the front.
    new_sys_path = [] 
    for item in list(sys.path): 
        if item not in prev_sys_path: 
            new_sys_path.append(item) 
            sys.path.remove(item) 
    sys.path[:0] = new_sys_path 


# Setup virtualenv
setup_venv(op.join(ROOT_DIR, 
    "venv/lib/python%s.%s/site-packages" %  sys.version_info[:2]))

# Gunicorn preferences
bind = "unix:/tmp/leechy.sock"
workers = os.sysconf("SC_NPROCESSORS_ONLN") * 2 + 1
worker_class = "gevent"
