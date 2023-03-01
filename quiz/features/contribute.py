from django.conf import settings
from lettuce import step, world
from lettuce.django import django_url
from lettuce.django import mail
from nose.tools import assert_equals


@step('I create a question')
def i_create_a_question(step):
    world.browser.visit(django_url('/quiz/create'))


@step('I should see the contribute form')
def i_should_see_the_contribute_form(step):
    assert world.browser.is_text_present('Create your own question', 3)


@step('I fill in "(.*)" as the question and "(.*)" as the explanation')
def i_fill_in_the_question_and_explanation(step, question, explanation):
    world.browser.fill('question', question)
    world.browser.fill('explanation', explanation)
    world.browser.find_by_name('to_moderation').click()


@step('The administrators should get an email about a new question')
def the_administrators_should_get_an_email_about_a_new_question(step):
    for admin in settings.ADMINS:
        message = mail.queue.get(True, timeout=5)
        assert admin[1] in message.recipients()
        assert 'Someone made a question' in message.subject


@step('I fill in the spam protection correctly')
def i_fill_in_the_spam_protection(step):
    world.browser.fill('spam_protection', 'human')


@step('I fill in the spam protection incorrectly')
def i_fill_in_the_spam_protection(step):
    world.browser.fill('spam_protection', 'spam-bot')
