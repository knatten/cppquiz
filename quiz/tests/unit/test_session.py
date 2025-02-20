import pytest
import unittest

import mock

from quiz.game_data import UserData, save_user_data
from quiz.tests.test_helpers import create_questions


pytestmark = pytest.mark.django_db


def create_session_with_answers_to(questions):
    session = {}
    user_data = UserData(session)

    for question in questions:
        user_data.register_correct_answer(question.pk)

    return user_data


class UserDataTest(unittest.TestCase):

    def test_given_new_session__has_no_correct_answers(self):
        user_data = create_session_with_answers_to(tuple())
        self.assertSetEqual(set(), user_data.get_correctly_answered_questions())

    def test_given_new_session__after_a_correct_answer_to_a_published_question_is_registered__it_is_listed_as_answered(self):
        [q1, q2] = create_questions(2, state='PUB')
        user_data = create_session_with_answers_to((q1,))
        self.assertSetEqual({q1.pk}, user_data.get_correctly_answered_questions())
        user_data.register_correct_answer(q2.pk)
        self.assertSetEqual({q1.pk, q2.pk}, user_data.get_correctly_answered_questions())

    def test_given_new_session__after_a_correct_answer_to_a_retracted_question_is_registered__it_is_not_listed_as_answered(self):
        [q] = create_questions(1, state='RET')
        user_data = create_session_with_answers_to((q,))
        self.assertSetEqual(set(), user_data.get_correctly_answered_questions())

    def test_given_new_session__after_a_published_question_becomes_retracted__its_answer_is_not_listed_as_answered(self):
        [q] = create_questions(1, state='PUB')
        user_data = create_session_with_answers_to((q,))
        self.assertSetEqual({q.pk}, user_data.get_correctly_answered_questions())
        q.state = 'RET'
        q.save()
        self.assertSetEqual(set(), user_data.get_correctly_answered_questions())

    def test_given_existing_session__correct_answers_are_still_there(self):
        [q] = create_questions(1)
        old_data = create_session_with_answers_to((q,))
        session = {'user_data': old_data}
        new_data = UserData(session)
        self.assertSetEqual({q.pk}, new_data.get_correctly_answered_questions())

    def test_clear_correct_answers(self):
        [q] = create_questions(1)
        user_data = create_session_with_answers_to((q,))
        self.assertSetEqual({q.pk}, user_data.get_correctly_answered_questions())
        user_data.clear_correct_answers()
        self.assertSetEqual(set(), user_data.get_correctly_answered_questions())


class save_user_dataTest(unittest.TestCase):

    def test_sets_modified(self):
        session = mock.MagicMock()
        save_user_data(None, session)
        self.assertTrue(session.modified)

    def test_sets_user_data(self):
        [q] = create_questions(1)
        session = mock.MagicMock()
        user_data = create_session_with_answers_to((q,))
        save_user_data(user_data, session)
        session.__setitem__.assert_called_once_with('user_data', user_data)

    def test_sets_expiry(self):
        session = mock.MagicMock()
        save_user_data(None, session)
        session.set_expiry.assert_called_once_with(315360000)
