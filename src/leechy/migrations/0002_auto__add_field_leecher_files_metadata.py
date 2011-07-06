# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Leecher.files_metadata'
        db.add_column('leechy_leecher', 'files_metadata', self.gf('leechy.fields.JSONField')(null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Leecher.files_metadata'
        db.delete_column('leechy_leecher', 'files_metadata')


    models = {
        'leechy.leecher': {
            'Meta': {'object_name': 'Leecher'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'files_metadata': ('leechy.fields.JSONField', [], {'null': 'True'}),
            'invitation_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'last_visit': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['leechy']
