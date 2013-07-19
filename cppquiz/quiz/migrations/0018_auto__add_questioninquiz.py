# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestionInQuiz'
        db.create_table('quiz_questioninquiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Question'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quiz.Quiz'])),
        ))
        db.send_create_signal('quiz', ['QuestionInQuiz'])

        # Removing M2M table for field questions on 'Quiz'
        db.delete_table('quiz_quiz_questions')


    def backwards(self, orm):
        # Deleting model 'QuestionInQuiz'
        db.delete_table('quiz_questioninquiz')

        # Adding M2M table for field questions on 'Quiz'
        db.create_table('quiz_quiz_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quiz', models.ForeignKey(orm['quiz.quiz'], null=False)),
            ('question', models.ForeignKey(orm['quiz.question'], null=False))
        ))
        db.create_unique('quiz_quiz_questions', ['quiz_id', 'question_id'])


    models = {
        'quiz.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'author_email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '254', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'explanation': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hint': ('django.db.models.fields.TextField', [], {'default': "'No hint'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '2'})
        },
        'quiz.questioninquiz': {
            'Meta': {'object_name': 'QuestionInQuiz'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Question']"}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Quiz']"})
        },
        'quiz.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '10'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['quiz.Question']", 'through': "orm['quiz.QuestionInQuiz']", 'symmetrical': 'False'})
        },
        'quiz.usersanswer': {
            'Meta': {'object_name': 'UsersAnswer'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '45', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['quiz.Question']"}),
            'result': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '2'})
        }
    }

    complete_apps = ['quiz']