# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Service.force_4326_support'
        db.add_column(u'geopapurls_service', 'force_4326_support',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Service.force_3857_support'
        db.add_column(u'geopapurls_service', 'force_3857_support',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Service.force_4326_support'
        db.delete_column(u'geopapurls_service', 'force_4326_support')

        # Deleting field 'Service.force_3857_support'
        db.delete_column(u'geopapurls_service', 'force_3857_support')


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
            'supports_3857': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supports_4326': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'geopapurls.service': {
            'Meta': {'object_name': 'Service'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bbox': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'force_3857_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'force_4326_support': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'getmapformats': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'getmapurl': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('geopapurls.models.WMSField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['geopapurls']