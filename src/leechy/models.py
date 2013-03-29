import uuid

from django.db import models
from django.core.urlresolvers import reverse

from leechy.fields import JSONField


class Leecher(models.Model):

    bool_metadata_attrs = ["checked"]
    bool_settings_attrs = ["hide_checked"]

    key = models.CharField(max_length=32, primary_key=True, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    enabled = models.BooleanField(default=True)
    invitation_sent = models.BooleanField(editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(editable=False, null=True)
    files_metadata = JSONField(editable=False, null=True)
    settings = JSONField(editable=False, null=True)

    def __unicode__(self):
        if self.name:
            return u"%s <%s>" % (self.name, self.email)
        return self.email

    def share_link(self):
        return '<a href="%(url)s">%(url)s</a>' % {
            "url": reverse("leechy_browse", 
                kwargs={"key": self.key, "path": ""})
        }
    share_link.allow_tags = True

    @classmethod
    def gen_key(cls, sender, instance, **_):
        if not instance.key:
            instance.key = str(uuid.uuid4()).replace("-", "")


models.signals.pre_save.connect(Leecher.gen_key, sender=Leecher)
