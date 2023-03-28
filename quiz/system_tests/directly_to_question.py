from quiz.system_tests.system_test_case import SystemTestCase
from quiz.test_helpers import create_questions


class StuffTest(SystemTestCase):
    def test_user_visits_the_site_root(self):
        create_questions(1)
        self.visit_root()
        self.should_end_up_at_a_question()

    def visit_root(self):
        self.visit('/')

    def should_end_up_at_a_question(self):
        self.assertIn('Question #', self.browser.html)
