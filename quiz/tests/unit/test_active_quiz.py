from django.test import TestCase

from quiz.active_quiz import ActiveQuiz
from quiz.fixed_quiz import create_quiz
from quiz.models import Quiz
from quiz.tests.test_helpers import create_questions


class ActiveQuizTest(TestCase):
    def test_shows_total_number_of_questions(self):
        create_questions(10)
        quiz = Quiz.objects.get(key=create_quiz(10))  # TODO maybe that method should return object instead of key
        active = ActiveQuiz(quiz)
        self.assertEqual(10, active.total_questions())
