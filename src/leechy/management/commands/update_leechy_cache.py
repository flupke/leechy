import os
import os.path as op

import pyinotify
import logging
from django.core.management.base import BaseCommand
from django.utils.encoding import force_unicode

from leechy import settings, cache


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # First fill the cache
        files_source = force_unicode(settings.FILES_SOURCE)
        logger.info(u"caching '%s'", files_source)
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
        logger.info(u"watching '%s' for changes", files_source)
        notifier.loop()
        
    def update_dir(self, event):
        path = force_unicode(event.pathname)
        logger.info(u"'%s' changed, updating its directory in cache", path)
        cache.cache_directory(op.dirname(path))
