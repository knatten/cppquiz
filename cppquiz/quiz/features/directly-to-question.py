from lettuce import step, world
from lettuce.django import django_url

@step('I should end up at a question')
def i_should_end_up_at_a_question(step):
    assert 'Question #' in world.browser.html
