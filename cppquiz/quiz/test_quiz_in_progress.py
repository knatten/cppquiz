from django.test import RequestFactory
from django.test import TestCase
import mock

from answer import Answer
from models import Quiz, Question
from fixed_quiz import create_quiz
from quiz_in_progress import QuizInProgress
from test_helpers import *

class QuizInProgressTest(TestCase):
    def set_up(self, nof_questions):
        create_questions(nof_questions)
        key = create_quiz(nof_questions)
        self.quiz = Quiz.objects.get(key=key)
        self.in_progress = QuizInProgress({}, self.quiz)

    def test_always__gives_correct_total_number_of_questions(self):
        self.set_up(10)
        self.assertEqual(10, self.in_progress.get_total_nof_questions())

    def test_given_new_quiz__returns_first_question_and_no_result_from_previous_question(self):
        self.set_up(10)
        self.assertEqual(self.quiz.questions.all()[0], self.in_progress.get_current_question())
        self.assertEqual(None, self.in_progress.get_previous_result())

    def test_when_answered_correctly__returns_next_question_and_previous_result_is_correct(self):
        self.set_up(10)
        self.answer_current_question_correctly()
        self.assertEqual(self.quiz.questions.all()[1], self.in_progress.get_current_question())
        self.assertEqual('correct', self.in_progress.get_previous_result())

    def test_when_answered_incorrectly__returns_same_question_and_previous_result_is_incorrect(self):
        self.set_up(10)
        self.answer_current_question_wrongly()
        self.assertEqual(self.quiz.questions.all()[0], self.in_progress.get_current_question())
        self.assertEqual('incorrect', self.in_progress.get_previous_result())

    def test_when_all_questions_are_answered__is_finished(self):
        self.set_up(1)
        self.assertFalse(self.in_progress.is_finished())
        self.answer_current_question_correctly()
        self.assertTrue(self.in_progress.is_finished())

    def answer_current_question_correctly(self):
        question = self.in_progress.get_current_question()
        request = RequestFactory().post('', data={'result' : question.result, 'answer' : question.answer})
        self.in_progress.answer(request)

    def answer_current_question_wrongly(self):
        question = self.in_progress.get_current_question()
        request = RequestFactory().post('', data={'result' : question.result, 'answer' : 'WRONG ANSWER'})
        self.in_progress.answer(request)
