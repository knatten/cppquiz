from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Question
from test_helpers import create_questions

class TrainingIntegrationTest(TestCase):
    def test_when_viewing_an_unpublished_question__gets_404(self):
        question = self.create_question(False)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_a_published_question__gets_it(self):
        question = self.create_question(True)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertContains(response, 'fluppa')

    def test_when_viewing_an_unpublished_question_with_a_preview_key__gets_it(self):
        question = self.create_question(False, 'abc123')
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}), {'preview_key': 'abc123'})
        self.assertContains(response, 'fluppa')

    def test_when_viewing_a_published_question_with_a_preview_key__gets_it(self):
        question = self.create_question(True, 'abc123')
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))#, 'preview_key': key}))
        self.assertContains(response, 'fluppa')

    def test_when_viewing_an_unpublished_question_with_a_wrong_preview_key__gets_404(self):
        question = self.create_question(False, 'abc123')
        response = self.client.get("/quiz/question/%d?preview_key=%s" % (question.pk, 'wrong'))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_an_unpublished_question_with_an_empty_preview_key__gets_404(self):
        question = self.create_question(False, '')
        response = self.client.get("/quiz/question/%d?preview_key=%s" % (question.pk, ''))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_an_unanswered_question__is_told_that_attempts_are_needed_before_giving_up_is_allowed(self):
        question = self.create_question(True)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertContains(response, 'make 3 more attempts first')

    def test_when_viewing_a_correctly_answered_question__is_not_told_about_giving_up(self):
        question = self.create_question(True)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}),
            {'did_answer': 'answer', 'result':question.result, 'answer':question.answer})
        self.assertContains(response, 'Correct')
        self.assertNotContains(response, 'more attempts first')

    def test_when_viewing_an_incorrectly_answered_question__is_told_that_more_attempts_are_needed_before_giving_up_is_allowed(self):
        question = self.create_question(True)
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertContains(response, 'make 3 more attempts first')
        response = self.answer_question_incorrectly(question)
        self.assertContains(response, 'make 2 more attempts first')
        response = self.answer_question_incorrectly(question)
        self.assertContains(response, 'make 1 more attempts first')
        response = self.answer_question_incorrectly(question)
        self.assertNotContains(response, 'more attempts first')

    def test_when_less_than_three_attempts_were_made__going_directly_to_the_giveup_page_is_not_allowed(self):
        question = self.create_question(True)
        response = self.client.get(reverse('quiz:giveup', kwargs={'question_id': question.pk}))
        self.assertEqual(404, response.status_code)

    def test_when_viewing_a_retracted_question__is_warned(self):
        question = self.create_question(True)
        question.retracted=True
        question.save()
        response = self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}))
        self.assertContains(response, 'This question has been retracted')

    def create_question(self, published, preview_key=''):
        return Question.objects.create(published=published, question='fluppa', answer='buppa', result='OK', hint='jotta', difficulty=1, preview_key=preview_key)

    def answer_question_incorrectly(self, question):
        return self.client.get(reverse('quiz:question', kwargs={'question_id': question.pk}),
            {'did_answer': 'answer', 'result':question.result, 'answer':'wrong'})
