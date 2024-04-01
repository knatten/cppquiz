from django.test import TestCase

from quiz.user_data import UserData
from quiz.util import get_correctly_answered_questions
from quiz.models import Question


class UtilTest(TestCase):

    def test_get_correctly_answered_questions(self):
        user_data = UserData()
        q = Question(state='PUB', hint='hint', difficulty=1)
        q.save()
        self.assertEquals(set(), get_correctly_answered_questions(user_data))
        user_data.register_correct_answer(q.pk)
        self.assertEqual(set((q.pk,)), get_correctly_answered_questions(user_data))
