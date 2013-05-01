import os
import os.path as op

import pyinotify
import logging
from django.core.management.base import BaseCommand

from leechy import settings, cache
from leechy.utils import force_utf8


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # First fill the cache
        files_source = force_utf8(settings.FILES_SOURCE)
        cache.cache_directory(files_source)
        for dirpath, dirnames, filenames in os.walk(files_source):
            for dirname in dirnames:
                cache.cache_directory(op.join(dirpath, dirname))
        # Then watch for changes
        manager = pyinotify.WatchManager()
        mask = (pyinotify.IN_DELETE | pyinotify.IN_CREATE |
                pyinotify.IN_MOVED_TO)
        manager.add_watch(files_source, mask, rec=True)
        notifier = pyinotify.Notifier(manager, self.update_dir)
        notifier.loop()
        
    def update_dir(self, event):
        path = force_utf8(event.pathname)
        cache.cache_directory(op.dirname(path))
