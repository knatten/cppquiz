from django.conf.urls import *

from quiz import api

urlpatterns = [
    url(r'^quiz', api.quiz, name='quiz'),
]
