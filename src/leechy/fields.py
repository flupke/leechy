from django.db import models
from django.utils import simplejson as json
from django.conf import settings

from south.modelsinspector import add_introspection_rules


class JSONField(models.TextField):

    def _dumps(self, data):
        return json.JSONEncoder().encode(data)

    def _loads(self, str):
        return json.loads(str, encoding=settings.DEFAULT_CHARSET)

    def db_type(self, connection):
        return 'text'

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        return self._dumps(value)

    def contribute_to_class(self, cls, name):
        self.class_name = cls
        super(JSONField, self).contribute_to_class(cls, name)
        models.signals.post_init.connect(self.post_init)

        def get_json(model_instance):
            return self._dumps(getattr(model_instance, self.attname, None))
        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, json):
            return setattr(model_instance, self.attname, self._loads(json))
        setattr(cls, 'set_%s_json' % self.name, set_json)

    def post_init(self, **kwargs):
        if 'sender' in kwargs and 'instance' in kwargs:
            if kwargs['sender'] == self.class_name and hasattr(kwargs['instance'], self.attname):
                value = self.value_from_object(kwargs['instance'])
                if (value):
                    setattr(kwargs['instance'], self.attname, self._loads(value))
                else:
                    setattr(kwargs['instance'], self.attname, None)


add_introspection_rules([], ["^leechy\.fields\.JSONField"])                    
