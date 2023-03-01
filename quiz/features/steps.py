from lettuce import step, world
from lettuce.django import django_url


@step('I visit (.+)')
def visit(step, url):
    world.browser.visit(django_url(url))


@step('There is an error "(.+)" in (.+)')
def there_is_an_error(step, error_msg, error_id):
    errors = world.browser.find_by_id(error_id + '_errors')[0]
    assert error_msg in errors.text
