# -*- coding: utf-8 -*-
import unittest

from .quiz_extras import *


class standard_ref_Test(unittest.TestCase):
    def test_given_no_reference(self):
        self.assertEqual('foo', standard_ref('foo'))

    def test_given_just_section(self):
        self.assertEqual(
            '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo">§[foo]</a></em>',
            standard_ref('§[foo]'))
        self.assertEqual(
            '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar">§[foo.bar]</a></em>',
            standard_ref('§[foo.bar]'))

    def test_given_section_and_paragraph(self):
        self.assertEqual(
            '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar#1.2">§[foo.bar]¶1.2</a></em>',
            standard_ref('§[foo.bar]¶1.2'))

    def test_doesnt_include_too_much(self):
        self.assertEqual('<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo.bar#1">§[foo.bar]¶1</a></em>.', standard_ref('§[foo.bar]¶1.'))

    def test_given_multiple_paragraphs(self):
        self.assertEqual(
            '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/foo">§[foo]</a></em>'
            '<em><a href="https://timsong-cpp.github.io/cppwp/n4659/bar">§[bar]</a></em>',
            standard_ref('§[foo]§[bar]'))
