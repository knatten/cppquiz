from django.conf.urls.defaults import *

from quiz import views

urlpatterns = patterns('',
    url(r'^quiz/question/(?P<question_id>.*)', views.question, name='question'),
    url(r'^$', views.index, name='index'),
)
