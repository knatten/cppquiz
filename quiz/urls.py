from django.urls import re_path
from django.views.generic.base import TemplateView

from quiz import views

app_name = 'quiz'
urlpatterns = [
    re_path(r'^quiz/question/(?P<question_id>\d+)', views.question, name='question'),
    re_path(r'^quiz/giveup/(?P<question_id>\d+)', views.giveup, name='giveup'),
    re_path(r'^quiz/clear', views.clear, name='clear'),
    re_path(r'^quiz/random', views.random_question, name='random'),
    re_path(r'^quiz/created', TemplateView.as_view(template_name='quiz/created.html')),
    re_path(r'^quiz/no_questions', TemplateView.as_view(template_name='quiz/no_questions.html')),
    re_path(r'^quiz/create', views.create, name='create'),
    re_path(r'^quiz/categorize', views.categorize, name='categorize'),
    re_path(r'^quiz/about', TemplateView.as_view(template_name='quiz/help.html')),
    re_path(r'^quiz/help', TemplateView.as_view(template_name='quiz/help.html')),
    re_path(r'^quiz/start', views.start, name='start'),
    re_path(r'^quiz/dismiss_training_msg', views.dismiss_training_msg, name='dismiss_training_msg'),
    re_path(r'^q/(?P<quiz_key>\w+)', views.quiz, name='quiz'),
    re_path(r'^raise', views.raise_exception, name='raise_exception'),
    re_path(r'^$', views.index, name='index'),
]
