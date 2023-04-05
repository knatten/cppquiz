from quiz import fixed_quiz
from quiz.models import Quiz
from quiz.tests.system.system_test_case import SystemTestCase
from quiz.tests.test_helpers import create_questions


class FixedQuizzesTest(SystemTestCase):
    def test_user_is_offered_to_start_a_quiz(self):
        create_questions(fixed_quiz.nof_questions_in_quiz)
        self.visit_a_random_question()
        self.should_be_offered_to_start_a_quiz()

    def test_user_who_mistypes_a_quiz_url_gets_suggestions(self):
        self.mistype_a_quiz_url()
        self.should_see_suggestions_for_quizzes_with_similar_keys()

    def visit_a_random_question(self):
        self.visit('/quiz/random')

    def should_be_offered_to_start_a_quiz(self):
        link = self.browser.links.find_by_text('Start a new quiz').first
        self.assertTrue(link)
        link.click()

    def mistype_a_quiz_url(self):
        Quiz.objects.create(key='abcde')
        self.visit('/q/abcdE')

    def should_see_suggestions_for_quizzes_with_similar_keys(self):
        self.assertTrue(self.browser.is_text_present('Quiz not found'))
        self.assertTrue(self.browser.is_text_present('abcde'))
