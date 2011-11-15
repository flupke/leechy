import os
import os.path as op
import datetime
import re
import urllib
from leechy import settings


class Entry(object):
    """
    Base class for file and directory entries.

    *name* is the entry's file name, *full_path* its path on the disk, and
    *rel_path* its path relative to leechy root.
    """
    
    search_split_pattern = re.compile(r"[\s.,-]")

    def __init__(self, name, full_path, rel_path, size, timestamp, metadata):
        self.name = name
        self.full_path = full_path
        self.rel_path = rel_path
        self.size = size
        self.metadata = metadata
        self.timestamp = timestamp
        self.mtime = datetime.datetime.fromtimestamp(self.timestamp)

    def search_words(self):
        words = self.search_split_pattern.split(self.name.encode("utf8"))
        if "tags" in self.metadata:
            words += self.search_split_pattern.split(self.metadata["tags"])
        return [w for w in words if w.strip()]

    def google_url(self):
        words = self.search_words()
        for pattern in settings.GOOGLE_SEARCH_FILTERS:
            words = [w for w in words if not pattern.match(w)]
            if not words:
                break
        return "http://www.google.com/search?%s" % urllib.urlencode(
                {"q": " ".join(words)})

    def as_dict(self):
        return {
            "name": self.name,
            "rel_path": self.rel_path,
            "timestamp": self.timestamp,
        }


class File(Entry):

    def __init__(self, name, full_path, rel_path, size, timestamp, metadata, url):
        super(File, self).__init__(name, full_path, rel_path, size, timestamp, metadata)
        self.url = url

    def as_dict(self):
        ret = super(File, self).as_dict()
        ret["url"] = self.url
        ret["size"] = self.size
        return ret


class Directory(Entry):

    pass
