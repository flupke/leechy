import os


workers = os.sysconf("SC_NPROCESSORS_ONLN") * 2 + 1
worker_class = "gevent"
