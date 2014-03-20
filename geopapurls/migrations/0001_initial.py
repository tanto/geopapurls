# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Layer'
        db.create_table(u'geopapurls_layer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True)),
            ('bbox', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True)),
            ('max_scale', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('min_scale', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('crs', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geopapurls.Service'])),
        ))
        db.send_create_signal(u'geopapurls', ['Layer'])

        # Adding model 'Service'
        db.create_table(u'geopapurls_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('geopapurls.models.WMSField')(max_length=512)),
            ('bbox', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('getmapurl', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('getmapformats', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'geopapurls', ['Service'])


    def backwards(self, orm):
        # Deleting model 'Layer'
        db.delete_table(u'geopapurls_layer')

        # Deleting model 'Service'
        db.delete_table(u'geopapurls_service')


    models = {
        u'geopapurls.layer': {
            'Meta': {'object_name': 'Layer'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True'}),
            'crs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_scale': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'min_scale': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geopapurls.Service']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'geopapurls.service': {
            'Meta': {'object_name': 'Service'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'getmapformats': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'getmapurl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('geopapurls.models.WMSField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['geopapurls']