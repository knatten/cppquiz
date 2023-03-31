from django.conf import settings
from django.core import mail

from quiz.system_tests.system_test_case import SystemTestCase


class ContributingQuestionsTest(SystemTestCase):
    def test_user_contributes_a_valid_question(self):
        self.visit_the_contribution_page()
        self.should_see_the_contribution_form()
        self.fill_in_the_spam_protection_correctly()
        self.fill_in_the_question_and_explanation('foo', 'bar')
        self.the_administrators_should_get_an_email_about_a_new_question()

    def test_user_forgets_to_enter_the_question_itself(self):
        self.visit_the_contribution_page()
        self.should_see_the_contribution_form()
        self.fill_in_the_spam_protection_correctly()
        self.fill_in_the_question_and_explanation('', 'bar')
        self.there_is_an_error('This field can not be empty.', 'question')

    def test_user_forgets_to_enter_an_explanation(self):
        self.visit_the_contribution_page()
        self.should_see_the_contribution_form()
        self.fill_in_the_spam_protection_correctly()
        self.fill_in_the_question_and_explanation('foo', '')
        self.there_is_an_error('This field can not be empty.', 'explanation')

    def test_user_contributes_a_valid_question_but_fails_spam_protection(self):
        self.visit_the_contribution_page()
        self.should_see_the_contribution_form()
        self.fill_in_the_spam_protection_incorrectly()
        self.fill_in_the_question_and_explanation('foo', 'bar')
        self.there_is_an_error('You failed the spam protection', 'spam_protection')

    def visit_the_contribution_page(self):
        self.visit('/quiz/create')

    def should_see_the_contribution_form(self):
        self.assertTrue(self.browser.is_text_present('Create your own question', 3))

    def fill_in_the_spam_protection_correctly(self):
        self.browser.fill('spam_protection', 'human')

    def fill_in_the_spam_protection_incorrectly(self):
        self.browser.fill('spam_protection', 'spam-bot')

    def fill_in_the_question_and_explanation(self, question, explanation):
        self.browser.fill('question', question)
        self.browser.fill('explanation', explanation)
        self.browser.find_by_name('to_moderation').click()

    def the_administrators_should_get_an_email_about_a_new_question(self):
        for admin in settings.ADMINS:
            message = mail.outbox.pop()
            self.assertIn(admin[1], message.to)
            self.assertIn('Someone made a question', message.subject)
