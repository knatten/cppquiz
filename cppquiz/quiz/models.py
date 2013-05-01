import datetime
from django.db import models

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
    explanation = models.TextField(default='', blank=True)
    date_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    published = models.BooleanField(default=True)
    author_email = models.EmailField(max_length=254, blank=True, default='')
    difficulty = models.IntegerField(default=0, choices=DIFFICULTY_CHOICES)

class UsersAnswer(models.Model):
    question = models.ForeignKey('Question')
    result = models.CharField(max_length=2, default='OK', choices=Question.RESULT_CHOICES)
    answer = models.CharField(max_length=200, default='', blank=True)
    ip = models.CharField(max_length=45, default='', blank=True)
    date_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    correct = models.BooleanField(default=False)
