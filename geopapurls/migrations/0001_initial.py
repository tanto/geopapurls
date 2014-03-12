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
            ('bbox', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geopapurls.Service'])),
        ))
        db.send_create_signal(u'geopapurls', ['Layer'])

        # Adding model 'Service'
        db.create_table(u'geopapurls_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('bbox', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('getmapurl', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('getmapformats', self.gf('django.db.models.fields.CharField')(max_length=255)),
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
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geopapurls.Service']"})
        },
        u'geopapurls.service': {
            'Meta': {'object_name': 'Service'},
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'getmapformats': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'getmapurl': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['geopapurls']