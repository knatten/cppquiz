from lettuce import step, world
from lettuce.django import django_url

@step('I visit the root of the site')
def i_visit_the_root(step):
    world.browser.visit(django_url('/'))
    pass

@step('I should end up at a question')
def i_should_end_up_at_a_question(step):
    assert 'Question #' in world.browser.html
