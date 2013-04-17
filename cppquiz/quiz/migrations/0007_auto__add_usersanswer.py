# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UsersAnswer'
        db.create_table('quiz_usersanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('answer', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(default='', max_length=45, blank=True)),
        ))
        db.send_create_signal('quiz', ['UsersAnswer'])


    def backwards(self, orm):
        
        # Deleting model 'UsersAnswer'
        db.delete_table('quiz_usersanswer')


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '2'})
        },
        'quiz.usersanswer': {
            'Meta': {'object_name': 'UsersAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Question']"})
        }
    }

    complete_apps = ['quiz']
