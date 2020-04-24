from django.conf.urls import *
from django.views.generic.base import TemplateView

from . import views

app_name='quiz'
urlpatterns = [
    url(r'^quiz/question/(?P<question_id>\d+)', views.question, name='question'),
    url(r'^quiz/giveup/(?P<question_id>\d+)', views.giveup, name='giveup'),
    url(r'^quiz/clear', views.clear, name='clear'),
    url(r'^quiz/random', views.random_question, name='random'),
    url(r'^quiz/created', TemplateView.as_view(template_name = 'quiz/created.html')),
    url(r'^quiz/no_questions', TemplateView.as_view(template_name = 'quiz/no_questions.html')),
    url(r'^quiz/create', views.create, name='create'),
    url(r'^quiz/categorize', views.categorize, name='categorize'),
    url(r'^quiz/about', TemplateView.as_view(template_name = 'quiz/help.html')),
    url(r'^quiz/help', TemplateView.as_view(template_name = 'quiz/help.html')),
    url(r'^quiz/start', views.start, name='start'),
    url(r'^quiz/dismiss_training_msg', views.dismiss_training_msg, name='dismiss_training_msg'),
    url(r'^system_info', views.show_system_info, name='system_info'),
    url(r'^q/(?P<quiz_key>\w+)', views.quiz, name='quiz'),
    url(r'^raise', views.raise_exception, name='raise_exception'),
    url(r'^$', views.index, name='index'),
]
