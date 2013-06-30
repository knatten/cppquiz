import re

from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Quiz, Question
from test_helpers import *
import fixed_quiz

class FixedQuizIntegrationTest(TestCase):
    def test_creating_a_quiz__creates_it_and_redirects_you_to_its_first_question(self):
        create_questions(30)
        response = self.client.get(reverse('quiz:start'))
        redirect = response.get('location')
        self.assertEqual(response.status_code, 302)

        redirect_relative = re.sub('http://\w*', '', redirect)
        response = self.client.get(redirect_relative)
        self.assertContains(response, 'You are taking quiz')
        self.assertRegexpMatches(response.content, 'You are taking quiz.*%s' % redirect_relative)

        first_question_in_quiz = Quiz.objects.all()[0].questions.all()[0].pk
        self.assertContains(response, 'Question #%d' % first_question_in_quiz)

        self.assert_status_string_with(response, 0,0)

    def test_correctly_answering_a_question_which_is_not_the_last__congratulates_you_and_takes_you_to_the_next_question(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        key = fixed_quiz.create_quiz(fixed_quiz.nof_questions_in_quiz)
        response = self.client.get(reverse('quiz:quiz', args=(key,)))
        pk = get_question_pk(response.content)
        response = self.answer_correctly(key, pk)
        self.assertContains(response, 'Correct!')
        self.assert_status_string_with(response, 1,1)

    def test_correctly_answering_the_last_question__takes_you_to_the_summary(self):
        create_questions(1)
        key = fixed_quiz.create_quiz(1)
        response = self.answer_correctly(key, 1)
        self.assertContains(response, 'Allright!')
        self.assert_result_string_with(response, 1)

    def assert_result_string_with(self, response, points):
        match = re.search('You finished the quiz, and got (\d+) points?.', response.content)
        self.assertTrue(match, 'Did not find result string')
        self.assertEqual(points, int(match.group(1)))

    def assert_status_string_with(self, response, answered, points):
        match = re.search('After (\d+) of (\d+) questions, you have (\d+) points', response.content)
        self.assertTrue(match, 'Did not find status string')
        self.assertEqual(answered, int(match.group(1)))
        self.assertEqual(fixed_quiz.nof_questions_in_quiz, int(match.group(2)))
        self.assertEqual(points, int(match.group(3)))

    def answer_correctly(self, key, question_pk):
        question = Question.objects.get(pk=question_pk)
        return self.client.post(
            reverse('quiz:quiz', args=(key,)),
            {'result':question.result, 'answer':question.answer},
            follow=True)
