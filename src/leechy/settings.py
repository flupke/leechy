from django.conf import settings
import os.path as op
from django.core.exceptions import ImproperlyConfigured


try:
    FILES_SOURCE = op.abspath(settings.LEECHY_FILES_SOURCE)
except AttributeError:
    raise ImproperlyConfigured("You must configure LEECHY_FILES_SOURCE in "
            "your settings")

try:
    FILES_ROOT = op.abspath(settings.LEECHY_FILES_ROOT)
except AttributeError:
    raise ImproperlyConfigured("You must configure LEECHY_FILES_ROOT in "
            "your settings")

try:
    FILES_URL = settings.LEECHY_FILES_URL
except AttributeError:
    raise ImproperlyConfigured("You must configure LEECHY_FILES_URL in "
            "your settings")
