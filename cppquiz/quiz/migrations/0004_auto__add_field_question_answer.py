# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Question.answer'
        db.add_column('quiz_question', 'answer', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Question.answer'
        db.delete_column('quiz_question', 'answer')


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['quiz']
