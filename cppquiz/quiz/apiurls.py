from django.conf.urls import *

import api

urlpatterns = [
    url(r'^quiz', api.quiz, name='quiz'),
]
