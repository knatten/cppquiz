from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

import views

urlpatterns = patterns('',
    url(r'^quiz/question/(?P<question_id>.+)', views.question, name='question'),
    url(r'^quiz/clear', views.clear, name='clear'),
    url(r'^quiz/random', views.random_question, name='random'),
    url(r'^quiz/created', TemplateView.as_view(template_name = 'quiz/created.html')),
    url(r'^quiz/create', views.create, name='create'),
    url(r'^quiz/categorize', views.categorize, name='categorize'),
    url(r'^quiz/about', TemplateView.as_view(template_name = 'quiz/help.html')),
    url(r'^quiz/help', TemplateView.as_view(template_name = 'quiz/help.html')),
    url(r'^quiz/start', views.start, name='start'),
    url(r'^quiz/dismiss_training_msg', views.dismiss_training_msg, name='dismiss_training_msg'),
    url(r'^q/(?P<quiz_key>.+)', views.quiz, name='quiz'),
    url(r'^$', views.index, name='index'),
)
