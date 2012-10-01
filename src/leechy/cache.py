import sys
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
    name = op.abspath(path.decode('utf8')).replace(u" ", u"_")
    return u"leechy-dir-cache-%s" % name


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
    for entry in os.listdir(path):
        entry = unicode(entry, 'utf8')
        for pattern in settings.EXCLUDE_FILES:
            if pattern.match(entry):
                continue
        entry_path = op.join(path, entry.encode('utf8'))
        if not op.exists(entry_path):
            # File was deleted during directory listing
            continue
        timestamp = op.getmtime(entry_path)
        if op.isdir(entry_path):
            size = 0
            for dirpath, dirnames, filenames in \
                    os.walk(entry_path):
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
    if op.exists(path):
        logger.debug("caching '%s'", cache_key)
        cache.set(cache_key, dir_cache_data(path))
    else:
        logger.debug("removing '%s' from cache", cache_key)
        cache.delete(cache_key)

