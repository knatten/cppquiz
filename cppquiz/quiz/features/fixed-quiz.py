# -*- coding: utf-8 -*-
from lettuce import step, world
from lettuce.django import django_url

@step(u'When I am answering random questions')
def when_i_am_answering_random_questions(step):
    world.browser.visit(django_url(''))

@step(u'Then I should be offered to start a quiz')
def then_i_should_be_offered_to_start_a_quiz(step):
    link = world.browser.find_link_by_text('Start a new quiz').first
    assert link
    link.click()
#    world.browser.click_link_by_text('Start a new quiz!')

