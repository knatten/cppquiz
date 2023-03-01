from lettuce import before, after, world
from splinter.browser import Browser
from django.test.utils import setup_test_environment, teardown_test_environment


@before.harvest
def initial_setup(server):
    world.browser = Browser()


@after.harvest
def cleanup(server):
    world.browser.quit()
