from lettuce import step, world
from lettuce.django import django_url

from cppquiz.quiz.models import Quiz


@step('When I am answering random questions')
def when_i_am_answering_random_questions(step):
    world.browser.visit(django_url(''))


@step('Then I should be offered to start a quiz')
def then_i_should_be_offered_to_start_a_quiz(step):
    link = world.browser.find_link_by_text('Start a new quiz').first
    assert link
    link.click()


@step('When I mistype a quiz')
def when_i_mistype_a_quiz(step):
    Quiz.objects.create(key='abcde')
    world.browser.visit(django_url('/q/abcdE'))


@step('Then I should see suggestions for quizzes with similar keys')
def then_i_should_see_suggestions_for_quizzes_with_similar_keys(step):
    assert world.browser.is_text_present('Quiz not found')
    assert world.browser.is_text_present('abcde')
