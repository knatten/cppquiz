import string

from django.test import TestCase

from quiz import fixed_quiz
from quiz.models import Quiz
from quiz.test_helpers import *


class get_unique_quiz_key_Test(TestCase):
    def test_returns_random_string(self):
        key = fixed_quiz.get_unique_quiz_key(5)
        self.assertEqual(5, len(key))
        self.assertEqual(type(''), type(key))

    def test_doesnt_reuse_a_key(self):
        number_of_possible_keys = len(string.ascii_uppercase + string.digits)
        keys = []
        for i in range(1, number_of_possible_keys):
            key = fixed_quiz.get_unique_quiz_key(1)
            Quiz.objects.create(key=key)
            self.assertNotIn(key, keys)
            keys.append(key)


class create_quiz_Test(TestCase):
    def test_creating_a_quiz_with_many_questions__has_correct_number_of_random_questions(self):
        create_questions(30)
        fixed_quiz.create_quiz(20)
        self.assertEqual(20, Quiz.objects.get(pk=1).questions.count())
        self.assertLooksKindOfRandom([q.id for q in Quiz.objects.get(pk=1).questions.all()])

    def test_creating_a_quiz_with_too_many_questions__throws(self):
        create_questions(1)
        self.assertRaises(ValueError, fixed_quiz.create_quiz, 2)

    def test_creating_a_quiz__gives_it_a_random_key(self):
        create_questions(10)
        key1 = fixed_quiz.create_quiz(1)
        key2 = fixed_quiz.create_quiz(2)
        self.assertNotEqual(key1, key2)
        self.assertEqual([key1, key2], [q.key for q in Quiz.objects.all()])

    def test_creating_a_quiz__has_questions_in_random_order(self):
        create_questions(10)
        fixed_quiz.create_quiz(10)
        pks = [q.pk for q in Quiz.objects.get(pk=1).get_ordered_questions()]
        self.assertNotEqual(sorted(pks), pks)

    def test_creating_a_quiz__only_uses_published_questions(self):
        [q0, q1, q2, q3] = create_questions(4)
        q0.state = 'NEW'
        q1.state = 'RET'
        q2.state = 'REF'
        q3.state = 'ACC'
        q0.save()
        q1.save()
        q2.save()
        q3.save()
        with self.assertRaises(ValueError):
            fixed_quiz.create_quiz(1)

    def assertLooksKindOfRandom(self, question_ids):
        # Only works if there are more questions in the db than we are asked to use in the quiz
        self.assertNotEqual(list(range(1, len(question_ids) + 1)), question_ids)
