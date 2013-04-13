# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PossibleAnswer'
        db.create_table('quiz_possibleanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('quiz', ['PossibleAnswer'])


    def backwards(self, orm):
        
        # Deleting model 'PossibleAnswer'
        db.delete_table('quiz_possibleanswer')


    models = {
        'quiz.possibleanswer': {
            'Meta': {'object_name': 'PossibleAnswer'},
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['quiz']
