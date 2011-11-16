import os
import os.path as op
import pyinotify
import logging
from django.core.management.base import BaseCommand
from leechy import settings, cache


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # First fill the cache
        logger.info("caching '%s'", settings.FILES_SOURCE)
        cache.cache_directory(settings.FILES_SOURCE)
        for dirpath, dirnames, filenames in os.walk(settings.FILES_SOURCE):
            for dirname in dirnames:
                cache.cache_directory(op.join(dirpath, dirname))
        # Then watch for changes
        manager = pyinotify.WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        manager.add_watch(settings.FILES_SOURCE, mask, rec=True)
        notifier = pyinotify.Notifier(manager, self.update_dir)
        logger.info("watching '%s' for changes", settings.FILES_SOURCE)
        notifier.loop()
        
    def update_dir(self, event):
        logger.info("'%s' changed, updating its directory in cache", event.pathname)
        cache.cache_directory(op.dirname(event.pathname))
