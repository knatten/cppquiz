import unittest

from quiz.user_data import UserData


class UserDataTest(unittest.TestCase):

    def test_new_object_has_no_data(self):
        user_data = UserData()
        self.assertFalse(user_data.dismissed_training_msg)
        self.assertEqual(0, user_data.attempts_given_for(13))

    def test_can_add_attempts(self):
        user_data = UserData()
        self.assertEqual(0, user_data.attempts_given_for(13))
        user_data.register_attempt(13)
        self.assertEqual(1, user_data.attempts_given_for(13))
        user_data.register_attempt(13)
        self.assertEqual(2, user_data.attempts_given_for(13))
        self.assertEqual(0, user_data.attempts_given_for(11))

    def test_can_add_and_clear_correct_answers(self):
        user_data = UserData()
        self.assertEqual(set(), user_data.get_correctly_answered_questions())
        user_data.register_correct_answer(1)
        user_data.register_correct_answer(2)
        self.assertEqual(set((1, 2)), user_data.get_correctly_answered_questions())
        user_data.clear_correct_answers()
        self.assertEqual(set(), user_data.get_correctly_answered_questions())

    def test_serialization(self):
        user_data = UserData()
        user_data.register_attempt(13)
        user_data.register_correct_answer(12)
        user_data.register_correct_answer(9)
        user_data.dismiss_training_msg()
        serialized = user_data.to_json()
        unserialized = user_data.from_json(serialized)
        self.assertEqual(unserialized.to_json(), serialized)
