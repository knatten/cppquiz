from django.contrib import admin
from quiz.models import *

def question_part(obj):
    return obj.question[:250] + '...'

class QuestionAdmin(admin.ModelAdmin):
    list_display=('pk', question_part, 'answer')

def question_pk(obj):
    return obj.question.pk

class UsersAnswerAdmin(admin.ModelAdmin):
    list_display=(question_pk, 'result', 'answer', 'correct', 'ip', 'date_time')

admin.site.register(Question, QuestionAdmin)
admin.site.register(UsersAnswer, UsersAnswerAdmin)
