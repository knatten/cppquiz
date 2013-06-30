import unittest

from fixed_quiz_test import *
from fixed_quiz_integration_test import *
from test_active_quiz import ActiveQuizTest
from test_quiz_in_progress import *

def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(get_unique_quiz_key_Test),
        unittest.TestLoader().loadTestsFromTestCase(create_quiz_Test),
        unittest.TestLoader().loadTestsFromTestCase(ActiveQuizTest),
        unittest.TestLoader().loadTestsFromTestCase(QuizInProgressTest),
        unittest.TestLoader().loadTestsFromTestCase(FixedQuizIntegrationTest),
        ])

