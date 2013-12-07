import unittest

from fixed_quiz_test import *
from fixed_quiz_integration_test import *
from test_active_quiz import ActiveQuizTest
from test_quiz_in_progress import *
from session_test import *
from templatetags.quiz_extras_test import *

def suite():
    return unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(get_unique_quiz_key_Test),
        unittest.TestLoader().loadTestsFromTestCase(create_quiz_Test),
        unittest.TestLoader().loadTestsFromTestCase(ActiveQuizTest),
        unittest.TestLoader().loadTestsFromTestCase(QuizInProgressTest),
        unittest.TestLoader().loadTestsFromTestCase(FixedQuizIntegrationTest),
        unittest.TestLoader().loadTestsFromTestCase(UserDataTest),
        unittest.TestLoader().loadTestsFromTestCase(save_user_dataTest),
        unittest.TestLoader().loadTestsFromTestCase(CodeTagsTest),
        unittest.TestLoader().loadTestsFromTestCase(standard_ref_Test),
        unittest.TestLoader().loadTestsFromTestCase(emphasize_test),
        ])

