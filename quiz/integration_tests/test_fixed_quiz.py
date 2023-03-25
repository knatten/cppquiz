import re

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from quiz import fixed_quiz
from quiz.models import Quiz, UsersAnswer
from quiz.test_helpers import Question, create_questions, get_question_pk


class FixedQuizIntegrationTest(TestCase):
    def test_creating_a_quiz__creates_it_and_redirects_you_to_its_first_question(self):
        create_questions(30)
        response = self.client.get(reverse('quiz:start'))
        redirect = response.get('location')
        self.assertEqual(response.status_code, 302)

        redirect_relative = re.sub('https://\w*', '', redirect)
        response = self.client.get(redirect_relative)
        self.assertContains(response, 'You are taking quiz')
        self.assertRegex(str(response.content), 'You are taking quiz.*%s' % redirect_relative)

        first_question_in_quiz = Quiz.objects.all()[0].get_ordered_questions()[0].pk
        self.assertContains(response, 'Question #%d' % first_question_in_quiz)

        self.assert_status_string_with(response, 0, 0)

    def test_correctly_answering_a_question_which_is_not_the_last__congratulates_you_and_takes_you_to_the_next_question(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        key = fixed_quiz.create_quiz()
        response = self.client.get(reverse('quiz:quiz', args=(key,)))
        pk = get_question_pk(str(response.content))
        response = self.answer_correctly(key, pk)
        self.assertContains(response, 'Correct!')
        explanation = Question.objects.get(pk=pk).explanation
        self.assertContains(response, explanation)
        self.assert_status_string_with(response, 1, 1)
        self.assertEqual(1, UsersAnswer.objects.count())

    def test_incorrectly_answering_a_question__redisplays_it_with_a_message_and_an_option_to_skip_it(self):
        create_questions(1)
        key = fixed_quiz.create_quiz(1)
        response = self.answer_incorrectly(key)
        self.assertContains(response, 'Incorrect!')
        self.assertEqual(1, UsersAnswer.objects.count())

    def test_skipping_a_question__takes_you_to_the_next_question_but_gives_you_no_points(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        key = fixed_quiz.create_quiz()
        quiz = Quiz.objects.get(key=key)
        response = self.answer_correctly(key, quiz.get_ordered_questions()[0].pk)
        self.assert_status_string_with(response, answered=1, points=1)
        users_answers_before_skipping = UsersAnswer.objects.count()
        response = self.skip(key)
        self.assert_status_string_with(response, answered=2, points=1)
        self.assertEqual(users_answers_before_skipping, UsersAnswer.objects.count())

    def test_asking_for_a_hint__displays_the_hint_but_takes_away_half_a_point(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        key = fixed_quiz.create_quiz()
        quiz = Quiz.objects.get(key=key)
        response = self.client.get(reverse('quiz:quiz', args=(key,)))
        self.assertContains(response, '>a hint<')
        self.assertContains(response, 'Hint', count=0)

        response = self.client.get(reverse('quiz:quiz', args=(key,)), {'hint': '1'})
        self.assertContains(response, '>a hint<', count=0)
        self.assertContains(response, 'Hint')
        response = self.answer_correctly(key, quiz.get_ordered_questions()[0].pk)
        self.assert_status_string_with(response, answered=1, points=0.5)

    def test_correctly_answering_the_last_question__takes_you_to_the_summary(self):
        create_questions(1)
        key = fixed_quiz.create_quiz(1)
        response = self.answer_correctly(key, 1)
        self.assertContains(response, 'All right!')
        self.assert_result_string_with(response, 1)
        self.assertEqual(1, UsersAnswer.objects.count())
        explanation = Quiz.objects.get(key=key).get_ordered_questions()[0].explanation
        self.assertContains(response, explanation)

    def test_skipping_the_last_question__takes_you_to_the_summary(self):
        create_questions(1)
        key = fixed_quiz.create_quiz(1)
        response = self.skip(key)
        self.assertContains(response, 'All right!')
        self.assert_result_string_with(response, 0)
        self.assertEqual(0, UsersAnswer.objects.count())
        self.assertNotContains(response, 'Correct')

    def test_when_a_session_exists_with_a_different_key__the_old_state_is_deleted(self):
        create_questions(20)
        key1 = fixed_quiz.create_quiz(fixed_quiz.nof_questions_in_quiz)
        key2 = fixed_quiz.create_quiz(fixed_quiz.nof_questions_in_quiz)
        quiz1 = Quiz.objects.get(key=key1)
        quiz2 = Quiz.objects.get(key=key2)
        response = self.answer_correctly(key1, quiz1.get_ordered_questions()[0].pk)
        self.assert_status_string_with(response, answered=1, points=1)
        response = self.client.get(reverse('quiz:quiz', args=(key2,)))
        self.assert_status_string_with(response, answered=0, points=0)

    def test_when_viewing_a_question__it_gets_timestamped(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        key = fixed_quiz.create_quiz()
        response = self.client.get(reverse('quiz:quiz', args=(key,)))
        pk = get_question_pk(str(response.content))
        self.assertLess((timezone.now() - Question.objects.get(pk=pk).last_viewed).total_seconds(), 10)

    def assert_result_string_with(self, response, points):
        match = re.search('You finished with (\d+.\d+) out of (\d+.\d+) .*possible.*points.', str(response.content))
        self.assertTrue(match, 'Did not find result string')
        self.assertEqual(points, float(match.group(1)))

    def assert_status_string_with(self, response, answered, points):
        match = re.search("After (\d+) of (\d+) questions, you have (\d+.\d+) .*points", str(response.content))
        self.assertTrue(match, 'Did not find status string')
        self.assertEqual(answered, int(match.group(1)),
                         'Expected to have answered %d question(s), but status is "%s"' % (answered, match.group(0)))
        self.assertEqual(fixed_quiz.nof_questions_in_quiz, int(match.group(
            2)), 'Expected to have a total of %d question(s), but status is "%s"' % (fixed_quiz.nof_questions_in_quiz, match.group(0)))
        self.assertEqual(points, float(match.group(3)),
                         'Expected to have %f point(s), but status is "%s"' % (points, match.group(0)))

    def answer_correctly(self, key, question_pk):
        question = Question.objects.get(pk=question_pk)
        return self.client.get(
            reverse('quiz:quiz', args=(key,)),
            {'result': question.result, 'answer': question.answer, 'did_answer': 'Answer'},
            follow=True)

    def answer_incorrectly(self, key):
        return self.client.get(
            reverse('quiz:quiz', args=(key,)),
            {'result': 'NONSENSE', 'answer': 'WROOOONG', 'did_answer': 'Answer'},
            follow=True)

    def skip(self, key):
        return self.client.get(
            reverse('quiz:quiz', args=(key,)),
            {'skip': 1})
