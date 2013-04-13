from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


from quiz import views

urlpatterns = patterns('',
    url(r'^quiz/question/(?P<question_id>.*)', views.question, name='question'),
    url(r'^quiz/clear', views.clear, name='clear'),
    url(r'^quiz/about', direct_to_template, {'template': 'quiz/help.html'}),
    url(r'^quiz/help', direct_to_template, {'template': 'quiz/help.html'}),
    url(r'^$', views.index, name='index'),
)
