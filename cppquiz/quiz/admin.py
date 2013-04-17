from django.contrib import admin
from quiz.models import *

def question_part(obj):
    return obj.question[:250] + '...'

class QuestionAdmin(admin.ModelAdmin):
    list_display=('pk', question_part, 'answer')

admin.site.register(Question, QuestionAdmin)
