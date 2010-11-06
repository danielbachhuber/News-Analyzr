# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Headquarters'
        db.create_table('dbpedia_headquarters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbpedia', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('loc_lat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('loc_long', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('dbpedia', ['Headquarters'])


    def backwards(self, orm):
        
        # Deleting model 'Headquarters'
        db.delete_table('dbpedia_headquarters')


    models = {
        'dbpedia.headquarters': {
            'Meta': {'object_name': 'Headquarters'},
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'loc_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'loc_long': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'dbpedia.language': {
            'Meta': {'object_name': 'Language'},
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dbpedia.literal': {
            'Meta': {'object_name': 'Literal'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'dbpedia.newsorg': {
            'Meta': {'object_name': 'NewsOrg'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'circulation': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbpedia.PrintFormat']", 'null': 'True'}),
            'headquarters': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbpedia.Language']", 'null': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'newsorg_links'", 'symmetrical': 'False', 'to': "orm['dbpedia.Value']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbpedia.Owner']", 'null': 'True', 'blank': 'True'}),
            'wikipedia': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'dbpedia.owner': {
            'Meta': {'object_name': 'Owner'},
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'dbpedia.printformat': {
            'Meta': {'object_name': 'PrintFormat'},
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'dbpedia.value': {
            'Meta': {'object_name': 'Value'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['dbpedia']
