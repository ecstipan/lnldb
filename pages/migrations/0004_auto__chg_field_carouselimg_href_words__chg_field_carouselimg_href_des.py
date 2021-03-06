# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CarouselImg.href_words'
        db.alter_column('pages_carouselimg', 'href_words', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'CarouselImg.href_desc'
        db.alter_column('pages_carouselimg', 'href_desc', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Changing field 'CarouselImg.href'
        db.alter_column('pages_carouselimg', 'href_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'], null=True))

    def backwards(self, orm):

        # Changing field 'CarouselImg.href_words'
        db.alter_column('pages_carouselimg', 'href_words', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Changing field 'CarouselImg.href_desc'
        db.alter_column('pages_carouselimg', 'href_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=64))

        # Changing field 'CarouselImg.href'
        db.alter_column('pages_carouselimg', 'href_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['pages.Page']))

    models = {
        'pages.carouselimg': {
            'Meta': {'object_name': 'CarouselImg'},
            'href': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']", 'null': 'True', 'blank': 'True'}),
            'href_desc': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'href_words': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'internal_name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imgs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pages.CarouselImg']", 'symmetrical': 'False'}),
            'main_nav': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['pages']