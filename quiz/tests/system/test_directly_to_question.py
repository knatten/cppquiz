from quiz.tests.system.system_test_case import SystemTestCase
from quiz.tests.test_helpers import create_questions


class DirectlyToQuestionTest(SystemTestCase):
    def test_user_visits_the_root_page(self):
        create_questions(1)
        self.visit_the_root_page()
        self.should_end_up_at_a_question()

    def visit_the_root_page(self):
        self.visit('/')

    def should_end_up_at_a_question(self):
        self.assertIn('Question #', self.browser.html)
