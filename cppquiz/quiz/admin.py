from django.contrib import admin
from quiz.models import *

def question_part(obj):
    return obj.question[:250]

class QuestionAdmin(admin.ModelAdmin):
    list_display=('pk', question_part, 'answer', 'published', 'difficulty')
    list_filter=('published', 'difficulty')
    search_fields=('question', 'explanation')

class UsersAnswerAdmin(admin.ModelAdmin):
    list_display=('question', 'result', 'answer', 'correct', 'ip', 'date_time')
    list_filter=('question',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(UsersAnswer, UsersAnswerAdmin)
