from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from .models import Question

class QuestionTest(TestCase):
    @parameterized.expand([
        ('PUB','publish'),
        ('SCH','schedule'),
    ])
    def test_limits_state_of_questions_without_difficulty_setting(self, state, verb):
        q = Question(state=state, hint = 'hint', difficulty=0)
        with self.assertRaises(ValidationError) as cm:
            q.save()
        self.assertIn(f'Cannot {verb} a question without a difficulty setting', str(cm.exception))

    @parameterized.expand([
        ('PUB','publish'),
        ('SCH','schedule'),
    ])
    def test_limits_state_of_questions_without_hint(self, state, verb):
        q = Question(state=state, hint = '', difficulty=1)
        with self.assertRaises(ValidationError) as cm:
            q.save()
        self.assertIn(f'Cannot {verb} a question without a hint', str(cm.exception))

    @parameterized.expand([
        ('PUB','publish'),
        ('SCH','schedule'),
    ])
    def test_limits_state_of_reserved_questions(self, state, verb):
        q = Question(state=state, hint = 'hint', difficulty=1, reserved=True)
        with self.assertRaises(ValidationError) as cm:
            q.save()
        self.assertIn(f'Cannot {verb} a reserved question', str(cm.exception))

    def test_is_allowed_to_save_unpublished_questions_without_hint_or_difficulty(self):
        q = Question(question='foo')
        q.save()
        self.assertEqual('foo', Question.objects.get(pk=q.pk).question)

    def test_questions_get_a_random_preview_key(self):
        q = Question.objects.create()
        self.assertEqual(10, len(q.preview_key))
        q2 = Question.objects.create()
        self.assertNotEqual(q.preview_key, q2.preview_key)
