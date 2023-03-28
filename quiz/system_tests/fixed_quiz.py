from quiz import fixed_quiz
from quiz.models import Quiz
from quiz.system_tests.system_test_case import SystemTestCase
from quiz.test_helpers import create_questions


class FixedQuizzesTest(SystemTestCase):
    def test_user_is_offered_to_start(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        self.answer_random_questions()
        self.should_be_offered_to_start_a_quiz()

    def test_user_who_mistypes_a_quiz_url_gets_suggestions(self):
        self.mistype_a_quiz()
        self.should_see_suggestions_for_quizzes_with_similar_keys()

    def answer_random_questions(self):
        self.visit('')

    def should_be_offered_to_start_a_quiz(self):
        link = self.browser.links.find_by_text('Start a new quiz').first
        assert link
        link.click()

    def mistype_a_quiz(self):
        Quiz.objects.create(key='abcde')
        self.visit('/q/abcdE')

    def should_see_suggestions_for_quizzes_with_similar_keys(self):
        assert self.browser.is_text_present('Quiz not found')
        assert self.browser.is_text_present('abcde')
