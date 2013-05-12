import unittest

from quiz_extras import code_tags

class CodeTagsTest(unittest.TestCase):

    def test_no_code(self):
        self.assertEqual('foo', code_tags('foo'))

    def test_with_code(self):
        self.assertEqual('foo<code>bar</code>baz', code_tags('foo`bar`baz'))

    def test_with_more_code(self):
        self.assertEqual('foo<code>bar</code>baz<code>flupp</code>', code_tags('foo`bar`baz`flupp`'))
