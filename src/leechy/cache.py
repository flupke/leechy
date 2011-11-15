import os
import os.path as op
from django.core.cache import cache
from leechy import settings


def dir_cache_key(path):
    return "leechy-dir-cache-%s" % path


def listdir(path):
    """
    Retrieve the contents of directory at *path*.
    """
    cached = cache.get(dir_cache_key(path))
    if cached is not None:
        return cached
    return dir_cache_data(path)


def dir_cache_data(path):
    """
    Return the data to store in the cache for directory at *path*.
    """
    files = []
    directories = []
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
    cache.set(dir_cache_key(path), dir_cache_data(path))
