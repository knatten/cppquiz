from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Question
from test_helpers import create_questions

class TrainingIntegrationTest(TestCase):
    def test_when_viewing_an_unpublished_question__gets_404(self):
        question = Question.objects.create(published=False, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_a_published_question__gets_it(self):
        question = Question.objects.create(published=True, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertContains(response, 'fluppa')

    def test_when_viewing_an_unpublished_question_with_a_preview_key__gets_it(self):
        key = 'abc123'
        question = Question.objects.create(published=False, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1, preview_key=key)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}), {'preview_key': key})
        self.assertContains(response, 'fluppa')

    def test_when_viewing_a_published_question_with_a_preview_key__gets_it(self):
        key = 'abc123'
        question = Question.objects.create(published=True, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1, preview_key=key)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))#, 'preview_key': key}))
        self.assertContains(response, 'fluppa')

    def test_when_viewing_an_unpublished_question_with_a_wrong_preview_key__gets_404(self):
        key = 'abc123'
        question = Question.objects.create(published=False, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1)
        response = self.client.get("/quiz/question/%d?preview_key=%s" % (question.pk, 'wrong'))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_an_unpublished_question_with_an_empty_preview_key__gets_404(self):
        key = ''
        question = Question.objects.create(published=False, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1, preview_key=key)
        response = self.client.get("/quiz/question/%d?preview_key=%s" % (question.pk, key))
        self.assertEqual(404, response.status_code)
