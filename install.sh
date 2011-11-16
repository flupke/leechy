#!/bin/sh
virtualenv --distribute venv
. venv/bin/activate
pip install -r requirements.txt
