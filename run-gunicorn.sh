#!/bin/sh
. venv/bin/activate
kill `cat var/run/gunicorn.pid`
cd sample_site
gunicorn_django --bind unix:/tmp/leechy.sock --daemon --pid ../var/run/gunicorn.pid --worker-class gevent --log-file ../var/log/leechy.log
