import unittest

from quiz.models import Question
from quiz.test_helpers import create_questions
from quiz.util import get_next_published_question, get_previous_published_question


class UtilTest(unittest.TestCase):

    def test_get_next_and_previous_question(self):
        questions = create_questions(2)  # Now we have at least two, other might already exist
        first_question = Question.objects.order_by("pk").first()
        last_question = Question.objects.order_by("pk").last()
        self.assertEqual(questions[1], get_next_published_question(questions[0]))
        self.assertEqual(None, get_next_published_question(last_question))
        self.assertEqual(questions[0], get_previous_published_question(questions[1]))
        self.assertEqual(None, get_previous_published_question(first_question))
