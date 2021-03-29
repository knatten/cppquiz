import json
from django.test import TestCase
from django.test.client import RequestFactory
from django.http import Http404

from .fixed_quiz import create_quiz
from .models import Quiz, Question
from .test_helpers import *

from . import api

class ApiTest(TestCase):
    def set_up(self, nof_questions=10):
        create_questions(nof_questions)
        self.key = create_quiz(nof_questions)
        self.quiz = Quiz.objects.get(key=self.key)

    def test_asking_for_existing_quiz_returns_ids(self):
        self.set_up()
        request = RequestFactory().get('_/?key=' + self.key)
        result = api.quiz(request)
        self.assertEqual(200, result.status_code)
        content = json.loads(result.content)
        self.assertEqual(
            [q.id for q in self.quiz.get_ordered_questions()],
            content['questions'])

    def test_asking_for_nonexisting_quiz_raises_404(self):
        request = RequestFactory().get('_/?key=this_key_should_not_exist')
        self.assertRaises(Http404, lambda:api.quiz(request))
