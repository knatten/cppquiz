import unittest

import mock

from quiz.game_data import UserData


def fake_answer(question_id):
    answer = mock.Mock()
    answer.question = answer.answer()
    answer.question.pk = str(question_id)
    return answer


class UserDataTest(unittest.TestCase):
    def test_when_no_attempts_given__says_no_attempts_given(self):
        u = UserData({})
        self.assertEqual(0, u.attempts_given_for(13))

    def test_reports_attempts_given(self):
        u = UserData({})
        u.register_attempt(fake_answer(13))
        self.assertEqual(1, u.attempts_given_for(13))

    def test_doesnt_report_answers_given_for_other_questions(self):
        u = UserData({})
        u.register_attempt(fake_answer(23))
        self.assertEqual(0, u.attempts_given_for(13))
