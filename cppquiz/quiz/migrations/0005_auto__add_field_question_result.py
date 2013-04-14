# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Question.result'
        db.add_column('quiz_question', 'result', self.gf('django.db.models.fields.CharField')(default='OK', max_length=2), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Question.result'
        db.delete_column('quiz_question', 'result')


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '2'})
        }
    }

    complete_apps = ['quiz']
