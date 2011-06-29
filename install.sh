#!/bin/sh
virtualenv --no-site-packages --distribute venv
. venv/bin/activate
pip install gunicorn django>=1.3 gevent
