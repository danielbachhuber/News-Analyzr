# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Literal'
        db.create_table('dbpedia_literal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dbpedia', ['Literal'])

        # Adding model 'Value'
        db.create_table('dbpedia_value', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('dbpedia', ['Value'])

        # Adding model 'NewsOrg'
        db.create_table('dbpedia_newsorg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbpedia', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('wikipedia', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('abstract', self.gf('django.db.models.fields.TextField')()),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbpedia.PrintFormat'], null=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbpedia.Language'], null=True)),
            ('circulation', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('owner', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('headquarters', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('dbpedia', ['NewsOrg'])

        # Adding M2M table for field links on 'NewsOrg'
        db.create_table('dbpedia_newsorg_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('newsorg', models.ForeignKey(orm['dbpedia.newsorg'], null=False)),
            ('value', models.ForeignKey(orm['dbpedia.value'], null=False))
        ))
        db.create_unique('dbpedia_newsorg_links', ['newsorg_id', 'value_id'])

        # Adding model 'Language'
        db.create_table('dbpedia_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbpedia', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dbpedia', ['Language'])

        # Adding model 'PrintFormat'
        db.create_table('dbpedia_printformat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbpedia', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('dbpedia', ['PrintFormat'])

        # Adding model 'Owner'
        db.create_table('dbpedia_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbpedia', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('dbpedia', ['Owner'])


    def backwards(self, orm):
        
        # Deleting model 'Literal'
        db.delete_table('dbpedia_literal')

        # Deleting model 'Value'
        db.delete_table('dbpedia_value')

        # Deleting model 'NewsOrg'
        db.delete_table('dbpedia_newsorg')

        # Removing M2M table for field links on 'NewsOrg'
        db.delete_table('dbpedia_newsorg_links')

        # Deleting model 'Language'
        db.delete_table('dbpedia_language')

        # Deleting model 'PrintFormat'
        db.delete_table('dbpedia_printformat')

        # Deleting model 'Owner'
        db.delete_table('dbpedia_owner')


    models = {
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
            'owner': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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
