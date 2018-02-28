from django.contrib import admin
from models import *

def question_part(obj):
    return obj.question[:250]

def result_short(obj):
    return obj.result

class QuestionAdmin(admin.ModelAdmin):
    list_display=('pk', 'published', 'retracted', 'refused', question_part, result_short, 'answer', 'difficulty', 'date_time')
    list_filter=('published', 'retracted', 'refused', 'difficulty', 'result')
    search_fields=('question', 'explanation')
    readonly_fields=('date_time',)

class UsersAnswerAdmin(admin.ModelAdmin):
    list_display=('question', 'result', 'answer', 'correct', 'ip', 'date_time')
    list_filter=('question',)

class QuizAdmin(admin.ModelAdmin):
    list_display=('key', 'date_time', 'question_ids')
    search_fields=('key',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(UsersAnswer, UsersAnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
