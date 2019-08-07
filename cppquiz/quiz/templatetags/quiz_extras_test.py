# -*- coding: utf-8 -*-
import unittest

from .quiz_extras import *


class standard_ref_Test(unittest.TestCase):
    def test_given_no_reference_doesnt_change(self):
        self.assertEqual('foo', standard_ref('foo'))

    def test_given_just_paragraph_references(self):
        self.assertEqual('<em>§3</em>', standard_ref('§3'))

    def test_given_sub_paragraph_references(self):
        self.assertEqual('<em>§3.45</em>', standard_ref('§3.45'))

    def test_given_pilcrow_references(self):
        self.assertEqual('<em>§33.44¶16.123</em>', standard_ref('§33.44¶16.123'))

    def test_given_name_references(self):
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo">[foo]\xa73.4</a></em>', standard_ref('[foo]§3.4'))
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo">[foo]\xa73.4</a></em>some_symbols', standard_ref('[foo]§3.4some_symbols'))
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#1">[foo.bar.baz]\xa73.4\xb61</a></em>', standard_ref('[foo.bar.baz]§3.4¶1'))

    def test_doesnt_include_too_much(self):
        self.assertEqual('<em>§3.4¶1</em>.', standard_ref('§3.4¶1.'))
        self.assertEqual('(<em>§3.4</em>)', standard_ref('(§3.4)'))

    def test_given_multiple_paragraphs(self):
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo">[foo]\xa73.4</a></em>, '
                         '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#1">[foo.bar.baz]\xa73.4\xb61</a></em>',
                          standard_ref('[foo]§3.4, [foo.bar.baz]§3.4¶1'))
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#1">[foo.bar.baz]\xa73.4\xb61</a></em>, '
                         '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#16">[foo.bar.baz]\xa73.4\xb616</a></em>',
                          standard_ref('[foo.bar.baz]§3.4¶1, [foo.bar.baz]§3.4¶16'))
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#16">[foo.bar.baz]\xa73.4\xb616</a></em>, '
                         '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#1">[foo.bar.baz]\xa73.4\xb61</a></em>',
                          standard_ref('[foo.bar.baz]§3.4¶16, [foo.bar.baz]§3.4¶1'))
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#16">[foo.bar.baz]\xa73.4\xb616</a></em>, '
                         '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar.baz#16">[foo.bar.baz]\xa73.4\xb616</a></em>',
                          standard_ref('[foo.bar.baz]§3.4¶16, [foo.bar.baz]§3.4¶16'))
