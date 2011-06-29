from django.db import models
import uuid


class Leecher(models.Model):

    key = models.CharField(max_length=32, primary_key=True, editable=False)
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True)
    enabled = models.BooleanField(default=True)
    invitation_sent = models.BooleanField(editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        if self.name:
            return u"%s <%s>" % (self.name, self.email)
        return self.email

    @classmethod
    def gen_key(cls, sender, instance, **_):
        if not instance.key:
            instance.key = str(uuid.uuid1()).replace("-", "")


models.signals.pre_save.connect(Leecher.gen_key, sender=Leecher)
