import unittest

import pytest
import mock

from quiz.game_data import UserData

pytestmark = pytest.mark.django_db


def fake_answer(question_id):
    answer = mock.Mock()
    answer.question = answer.answer()
    answer.question.pk = str(question_id)
    return answer


class UserDataTest(unittest.TestCase):
    def test_when_no_attempts_given__says_no_attempts_given(self):
        u = UserData()
        self.assertEqual(0, u.attempts_given_for(13))

    def test_reports_attempts_given(self):
        u = UserData()
        u.register_attempt(fake_answer(13))
        self.assertEqual(1, u.attempts_given_for(13))

    def test_doesnt_report_answers_given_for_other_questions(self):
        u = UserData()
        u.register_attempt(fake_answer(23))
        self.assertEqual(0, u.attempts_given_for(13))

    def test_to_from_dict(self):
        user_data = UserData()
        user_data.register_attempt(fake_answer(13))
        user_data.dismissed_training_msg = True
        user_data.register_correct_answer(17)
        serialized = user_data.to_dict()
        user_data2 = UserData.from_dict(serialized)
        self.assertEqual(user_data2.attempts_given_for(13), 1)
        self.assertEqual(user_data2.correctly_answered, {17})
        self.assertEqual(user_data2.dismissed_training_msg, True)
