import mock
import unittest

from quiz.game_data import *

class UserDataTest(unittest.TestCase):

    def test_given_new_session__has_no_correct_answers(self):
        session = {}
        s = UserData(session)
        self.assertSetEqual(set(), s.get_correctly_answered_questions())

    def test_given_new_session__after_a_correct_answer_is_registered__it_is_listed_as_answered(self):
        session = {}
        s = UserData(session)
        s.register_correct_answer(23)
        self.assertSetEqual({23}, s.get_correctly_answered_questions())
        s.register_correct_answer(4)
        self.assertSetEqual({4, 23}, s.get_correctly_answered_questions())

    def test_given_existing_session__correct_answers_are_still_there(self):
        old_data = UserData({})
        old_data.register_correct_answer(16)
        session = {'user_data' : old_data}
        new_data = UserData(session)
        self.assertSetEqual({16}, new_data.get_correctly_answered_questions())

    def test_clear_correct_answers(self):
        s = UserData({})
        s.register_correct_answer(23)
        s.clear_correct_answers()
        self.assertSetEqual(set(), s.get_correctly_answered_questions())

        

class save_user_dataTest(unittest.TestCase):
    
        def test_sets_modified(self):
            session = mock.MagicMock()
            save_user_data(None, session)
            self.assertTrue(session.modified)
    
        def test_sets_user_data(self):
            session = mock.MagicMock()
            user_data = UserData({})
            user_data.register_correct_answer(53)
            save_user_data(user_data, session)
            session.__setitem__.assert_called_once_with('user_data', user_data)

        def test_sets_expiry(self):
            session = mock.MagicMock()
            save_user_data(None, session)
            session.set_expiry.assert_called_once_with(315360000)
