# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Headquarters.country'
        db.add_column('dbpedia_headquarters', 'country', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'Headquarters.region'
        db.add_column('dbpedia_headquarters', 'region', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Headquarters.country'
        db.delete_column('dbpedia_headquarters', 'country')

        # Deleting field 'Headquarters.region'
        db.delete_column('dbpedia_headquarters', 'region')


    models = {
        'dbpedia.headquarters': {
            'Meta': {'object_name': 'Headquarters'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dbpedia': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'loc_lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'loc_long': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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
