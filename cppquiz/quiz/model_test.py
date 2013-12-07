from django.core.exceptions import ValidationError
from django.test import TestCase

from models import Question

class QuestionTest(TestCase):
    def test_is_not_allowed_to_save_published_questions_without_difficulty(self):
        q = Question(published=True, hint = 'hint', difficulty=0)
        with self.assertRaises(ValidationError) as cm:
            q.save()
        self.assertIn('Cannot publish a question without a difficulty setting', str(cm.exception))

    def test_is_not_allowed_to_save_published_questions_without_hint(self):
        q = Question(published=True, hint = '', difficulty=1)
        with self.assertRaises(ValidationError) as cm:
            q.save()
        self.assertIn('Cannot publish a question without a hint', str(cm.exception))

    def test_is_allowed_to_save_unpublished_questions_without_hint_or_difficulty(self):
        q = Question(question='foo')
        q.save()
        self.assertEqual('foo', Question.objects.get(pk=q.pk).question)
