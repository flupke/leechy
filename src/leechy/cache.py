import os
import os.path as op
import logging
from django.core.cache import cache
from leechy import settings


logger = logging.getLogger(__name__)


def dir_cache_key(path):
    """
    Get the cache key for *path*.
    """
    return "leechy-dir-cache-%s" % op.abspath(path).replace(" ", "_")


def listdir(path):
    """
    Retrieve the contents of directory at *path*.
    """
    cache_key = dir_cache_key(path)
    data = cache.get(cache_key)
    if data is not None:
        logger.debug("cache hit: '%s'", cache_key)
        return data
    logger.debug("cache miss: '%s'", cache_key)
    return dir_cache_data(path)


def dir_cache_data(path):
    """
    Return the data to store in the cache for directory at *path*.
    """
    files = []
    directories = []
    if not isinstance(path, unicode):
        path = unicode(path, "utf8")
    for entry in os.listdir(path):
        for pattern in settings.EXCLUDE_FILES:
            if pattern.match(entry):
                continue
        entry_path = op.join(path, entry)
        timestamp = op.getmtime(entry_path)
        if op.isdir(entry_path):
            size = 0
            for dirpath, dirnames, filenames in os.walk(entry_path):
                for f in filenames:
                    fp = op.join(dirpath, f)
                    if op.exists(fp):
                        size += op.getsize(fp)
            directories.append((entry, size, timestamp))
        else:
            size = op.getsize(entry_path)
            files.append((entry, size, timestamp))
    return directories, files


def cache_directory(path):
    """
    Put the directory at *path* in the cache.
    """
    cache_key = dir_cache_key(path)
    logger.debug("caching '%s'", cache_key)
    cache.set(cache_key, dir_cache_data(path))
