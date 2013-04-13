# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'PossibleAnswer'
        db.delete_table('quiz_possibleanswer')


    def backwards(self, orm):
        
        # Adding model 'PossibleAnswer'
        db.create_table('quiz_possibleanswer', (
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('quiz', ['PossibleAnswer'])


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['quiz']
