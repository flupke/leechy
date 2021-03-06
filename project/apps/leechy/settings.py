import os.path as op
import re

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
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

INNKEEPER_NAME = getattr(settings, "LEECHY_INNKEEPER_NAME", _("Your friend"))

INVITATION_SUBJECT = getattr(settings, "LEECHY_INVITATION_SUBJECT", 
    _("%(innkeeper_name)s has invited you to browse its files") %
    {"innkeeper_name": INNKEEPER_NAME})

INVITATION_EMAIL_FROM = getattr(settings, "LEECHY_INVITATION_EMAIL_FROM", 
    "leechy@host.com")

EXCLUDE_FILES = getattr(settings, "LEECHY_EXCLUDE_FILES", ["^\..*"])
EXCLUDE_FILES = [p if hasattr(p, "match") else re.compile(p) 
        for p in EXCLUDE_FILES]

GOOGLE_SEARCH_FILTERS = getattr(settings, "LEECHY_GOOGLE_SEARCH_FILTERS", [])
GOOGLE_SEARCH_FILTERS = [p if hasattr(p, "match") else re.compile(p) 
        for p in GOOGLE_SEARCH_FILTERS]

SHOUTBOX_BACKLOG = getattr(settings, "LEECHY_SHOUTBOX_BACKLOG", 100)
