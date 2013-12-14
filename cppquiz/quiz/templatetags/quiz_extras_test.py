# -*- coding: utf-8 -*-
import unittest

from quiz_extras import *

class CodeTagsTest(unittest.TestCase):

    def test_no_code(self):
        self.assertEqual('foo', code_tags('foo'))

    def test_with_code(self):
        self.assertEqual('foo<code>bar</code>baz', code_tags('foo`bar`baz'))

    def test_with_more_code(self):
        self.assertEqual('foo<code>bar</code>baz<code>flupp</code>', code_tags('foo`bar`baz`flupp`'))

class code_blocks_Test(unittest.TestCase):

    def test_no_code(self):
        self.assertEqual('foo', code_blocks('foo'))

    def test_code_in_the_middle_of_text(self):
        self.assertEqual(middle_of_text_result, code_blocks(middle_of_text))

    def test_code_in_the_beginning_of_text(self):
        self.assertEqual(beginning_of_text_result, code_blocks(beginning_of_text))

    def test_code_at_the_end_of_text(self):
        self.assertEqual(end_of_text_result, code_blocks(end_of_text))

    def test_several_code_block(self):
        self.assertEqual(several_code_blocks_result, code_blocks(several_code_blocks))

class standard_ref_Test(unittest.TestCase):
    def test_given_no_reference_doesnt_change(self):
        self.assertEqual('foo', standard_ref('foo'))

    def test_given_just_paragraph_references(self):
        self.assertEqual(u'<em>§3</em>', standard_ref(u'§3'))

    def test_given_sub_paragraph_references(self):
        self.assertEqual(u'<em>§3.4</em>', standard_ref(u'§3.4'))

    def test_given_pilcrow_references(self):
        self.assertEqual(u'<em>§3.4¶1</em>', standard_ref(u'§3.4¶1'))

    def test_doesnt_include_too_much(self):
        self.assertEqual(u'<em>§3.4¶1</em>.', standard_ref(u'§3.4¶1.'))

class emphasize_test(unittest.TestCase):
    def test(self):
        self.assertEqual('foo',  emphasize('foo'))
        self.assertEqual('<strong>foo</strong> bar',  emphasize('***foo*** bar'))


middle_of_text = """foo
    int i;
bar"""
middle_of_text_result = """foo
</p><pre class="sh_cpp sh_sourceCode">    int i;
</pre><p>bar"""

beginning_of_text = """    int i;
bar"""
beginning_of_text_result = """</p><pre class="sh_cpp sh_sourceCode">    int i;
</pre><p>bar"""

end_of_text = """foo
    int i;"""
end_of_text_result = """foo
</p><pre class="sh_cpp sh_sourceCode">    int i;</pre><p>"""

several_code_blocks = """foo
    int i;
    int j;
bar
    float x;
    float y;"""
several_code_blocks_result = """foo
</p><pre class="sh_cpp sh_sourceCode">    int i;
    int j;
</pre><p>bar
</p><pre class="sh_cpp sh_sourceCode">    float x;
    float y;</pre><p>"""
