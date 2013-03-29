import os.path as op
import datetime
import re
import urllib
from collections import defaultdict

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
        words = self.search_split_pattern.split(
                op.splitext(self.name.encode("utf8"))[0])
        words += ["[%s]" % w for w in self.tags]                    
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
            "tags": self.tags,
        }

    @property
    def tags(self):
        tags = self.search_split_pattern.split(self.metadata.get("tags", ""))
        tags = [w for w in tags if w.strip()]
        return set(tags)

    @classmethod
    def tags_cloud(cls, entries):
        tags = defaultdict(int)
        for entry in entries:
            for tag in entry.tags:
                tags[tag] += 1
        return dict(tags)


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
