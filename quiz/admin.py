from django.contrib import admin
from django.urls import reverse
from reversion.admin import VersionAdmin


from quiz.models import Question, Quiz, UsersAnswer, QuestionInQuiz


def question_part(obj):
    return obj.question[:250]


def result_short(obj):
    return obj.result


class QuestionAdmin(VersionAdmin):
    list_display = ('pk', 'state', 'author_email', 'reserved', 'reservation_message', question_part,
                    result_short, 'answer', 'difficulty', 'date_time', 'publish_time')
    list_filter = ('state', 'difficulty', 'result')
    search_fields = ('question', 'explanation')
    readonly_fields = ('date_time', 'last_viewed')

    def view_on_site(self, obj):
        return reverse('quiz:question', args=[obj.pk]) + "?preview_key=" + obj.preview_key


class UsersAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'result', 'answer', 'correct', 'date_time')
    list_filter = ('question',)


class QuizAdmin(admin.ModelAdmin):
    list_display = ('key', 'date_time', 'question_ids')
    search_fields = ('key',)


class QuestionInQuizAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)


admin.site.register(Question, QuestionAdmin)
admin.site.register(UsersAnswer, UsersAnswerAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionInQuiz, QuestionInQuizAdmin)
