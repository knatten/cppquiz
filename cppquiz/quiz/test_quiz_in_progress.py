from django.test import RequestFactory
from django.test import TestCase
import mock

from answer import Answer
from models import Quiz, Question
from fixed_quiz import create_quiz
from quiz_in_progress import QuizInProgress
from test_helpers import *

class QuizInProgressTest(TestCase):
    def set_up(self, nof_questions=10):
        create_questions(nof_questions)
        key = create_quiz(nof_questions)
        self.quiz = Quiz.objects.get(key=key)
        self.in_progress = QuizInProgress({}, self.quiz)

    def test_always__gives_correct_total_number_of_questions(self):
        self.set_up(10)
        self.assertEqual(10, self.in_progress.get_total_nof_questions())

    def test_given_new_quiz__returns_first_question_and_no_result_from_previous_question(self):
        self.set_up()
        self.assertEqual(self.quiz.get_ordered_questions()[0], self.in_progress.get_current_question())
        self.assertEqual(None, self.in_progress.get_previous_result())

    def test_when_answered_correctly__returns_next_question_and_previous_result_is_correct_and_explained(self):
        self.set_up()
        self.answer_current_question_correctly()
        self.assertEqual(self.quiz.get_ordered_questions()[1], self.in_progress.get_current_question())
        self.assertEqual('correct', self.in_progress.get_previous_result())
        explanation = self.quiz.get_ordered_questions()[0].explanation
        self.assertEqual(explanation, self.in_progress.get_previous_explanation())

    def test_when_answered_incorrectly__returns_same_question_and_previous_result_is_incorrect(self):
        self.set_up()
        self.answer_current_question_incorrectly()
        self.assertEqual(self.quiz.get_ordered_questions()[0], self.in_progress.get_current_question())
        self.assertEqual('incorrect', self.in_progress.get_previous_result())

    def test_when_skipped__returns_next_question_and_no_result_from_previous_question(self):
        self.set_up()
        self.in_progress.skip()
        self.assertEqual(self.quiz.get_ordered_questions()[1], self.in_progress.get_current_question())
        self.assertEqual(None, self.in_progress.get_previous_result())

    def test_when_skipped__clears_previous_result(self):
        self.set_up()
        for function in [self.answer_current_question_correctly, self.answer_current_question_incorrectly]:
            self.in_progress.skip()
            self.assertEqual(None, self.in_progress.get_previous_result())

    def test_when_all_questions_are_answered__is_finished(self):
        self.set_up(1)
        self.assertFalse(self.in_progress.is_finished())
        self.answer_current_question_correctly()
        self.assertTrue(self.in_progress.is_finished())

    def test_when_starting__count_and_score_are_zero(self):
        self.set_up()
        self.assertEqual(0, self.in_progress.nof_answered_questions())
        self.assertEqual(0, self.in_progress.score())

    def test_when_a_question_is_answered_correctly__count_and_score_are_one(self):
        self.set_up()
        self.answer_current_question_correctly()
        self.assertEqual(1, self.in_progress.nof_answered_questions())
        self.assertEqual(1, self.in_progress.score())

    def test_when_a_question_is_answered_incorrectly__count_and_score_are_zero(self):
        self.set_up()
        self.answer_current_question_incorrectly()
        self.assertEqual(0, self.in_progress.nof_answered_questions())
        self.assertEqual(0, self.in_progress.score())

    def test_when_skippting_a_question__count_is_one_but_score_is_zero(self):
        self.set_up()
        self.in_progress.skip()
        self.assertEqual(1, self.in_progress.nof_answered_questions())
        self.assertEqual(0, self.in_progress.score())

    def test_when_two_attempts_are_made__score_is_divided_by_two(self):
        self.set_up()
        self.answer_current_question_incorrectly()
        self.answer_current_question_correctly()
        self.assertEqual(.5, self.in_progress.score())

    def test_when_three_attempts_are_made__score_is_divided_by_eight(self):
        self.set_up()
        for i in range(0,3):
            self.answer_current_question_incorrectly()
        self.answer_current_question_correctly()
        self.assertEqual(1.0/8, self.in_progress.score())

    def test_when_hint_is_used__score_is_reduced_by_half_a_point(self):
        self.set_up()
        self.in_progress.use_hint()
        self.answer_current_question_correctly()
        self.assertEqual(.5, self.in_progress.score())

    def test_when_hint_is_used_and_question_is_answered_correctly__doesnt_affect_next_question(self):
        self.set_up()
        self.in_progress.use_hint()
        self.answer_current_question_correctly()
        self.answer_current_question_correctly()
        self.assertEqual(1.5, self.in_progress.score())

    def test_when_hint_is_used_and_question_is_skipped__doesnt_affect_next_question(self):
        self.set_up()
        self.in_progress.use_hint()
        self.in_progress.skip()
        self.answer_current_question_correctly()
        self.assertEqual(1, self.in_progress.score())

    def test_when_we_somehow_get_index_error__get_current_question_provides_good_info(self):
        self.set_up(2)
        for i in range(0,2):
            self.answer_current_question_correctly()
        try:
            self.in_progress.get_current_question()
            self.fail()
        except Exception as e:
            self.assertEqual("2 questions, 2 answers", str(e))

    def answer_current_question_correctly(self):
        question = self.in_progress.get_current_question()
        request = RequestFactory().post('', data={'result' : question.result, 'answer' : question.answer})
        self.in_progress.answer(request)

    def answer_current_question_incorrectly(self):
        question = self.in_progress.get_current_question()
        request = RequestFactory().post('', data={'result' : question.result, 'answer' : 'WRONG ANSWER'})
        self.in_progress.answer(request)
