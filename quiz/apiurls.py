from django.conf.urls import re_path

from quiz import api

urlpatterns = [
    re_path(r'^quiz', api.quiz, name='quiz'),
]
