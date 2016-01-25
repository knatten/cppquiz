 # -*- coding: utf-8 -*-
import datetime
import random
import string

from django.core.exceptions import ValidationError
from django.db import models

def generate_preview_key():
    return ''.join(random.sample(string.ascii_lowercase + string.digits, 10))

class Question(models.Model):
    RESULT_CHOICES = (
        ('OK', 'is compilable and deterministic'),
        ('CE', 'has a compilation error'),
        ('US', 'is unspecified'),
        ('UD', 'is undefined'),
    )
    DIFFICULTY_CHOICES = (
        (0, 'Not set'),
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Expert'),
    )
    question = models.TextField(default='', blank=True)
    result = models.CharField(max_length=2, default='OK', choices=RESULT_CHOICES)
    answer = models.CharField(max_length=200, default='', blank=True)
    explanation = models.TextField(default='', blank=True, help_text='Refer to the standard like this: §x.y¶z. Wrap code like this: `int i`. Wrap in stars to ***emphasize***')
    hint = models.TextField(default='No hint', blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    author_email = models.EmailField(max_length=254, blank=True, default='')
    difficulty = models.IntegerField(default=0, choices=DIFFICULTY_CHOICES)
    preview_key = models.CharField(blank=True, max_length=10, default=generate_preview_key)

    def __str__(self):
        return str(self.pk)

    def clean(self):
        if self.published and self.hint == '':
            raise ValidationError('Cannot publish a question without a hint')
        if self.published and self.difficulty == 0:
            raise ValidationError('Cannot publish a question without a difficulty setting')

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Question, self).save(*args, **kwargs)

class UsersAnswer(models.Model):
    question = models.ForeignKey('Question')
    result = models.CharField(max_length=2, default='OK', choices=Question.RESULT_CHOICES)
    answer = models.CharField(max_length=200, default='', blank=True)
    ip = models.CharField(max_length=45, default='', blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)

class Quiz(models.Model):
    questions = models.ManyToManyField(Question, through='QuestionInQuiz')
    key = models.CharField(max_length=10, default='')
    date_time = models.DateTimeField(auto_now_add=True)

    def get_ordered_questions(self):
        #Order pseudo-randomly but not in order of primary key
        return self.questions.all().order_by('hint', 'id')

    def question_ids(self):
        return ','.join([str(q) for q in self.questions.all()])

class QuestionInQuiz(models.Model):
    question = models.ForeignKey(Question)
    quiz = models.ForeignKey(Quiz)
