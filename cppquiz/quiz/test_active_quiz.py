from django.test import TestCase

from models import Quiz
from active_quiz import *
from fixed_quiz import *
from test_helpers import *

class ActiveQuizTest(TestCase):
    def test_shows_total_number_of_questions(self):
        create_questions(10)
        quiz = Quiz.objects.get(key=create_quiz(10)) #TODO maybe that method should return object instead of key
        active = ActiveQuiz(quiz)
        self.assertEqual(10, active.total_questions())
