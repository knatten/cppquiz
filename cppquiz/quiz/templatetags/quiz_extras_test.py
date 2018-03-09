# -*- coding: utf-8 -*-
import unittest

from quiz_extras import *


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
