import unittest

from quiz.templatetags.quiz_extras import standard_ref


class standard_ref_Test(unittest.TestCase):
    def test_given_no_reference(self):
        self.assertEqual('foo', standard_ref('foo'))

    def test_given_just_section(self):
        self.assertEqual(
            '*[§[foo]](https://timsong-cpp.github.io/cppwp/std23/foo)*',
            standard_ref('§[foo]'))
        self.assertEqual(
            '*[§[foo.bar]](https://timsong-cpp.github.io/cppwp/std23/foo.bar)*',
            standard_ref('§[foo.bar]'))
        self.assertEqual(
            '*[§[foo::bar]](https://timsong-cpp.github.io/cppwp/std23/foo::bar)*',
            standard_ref('§[foo::bar]'))

    def test_given_section_and_paragraph(self):
        self.assertEqual(
            '*[§[foo.bar]¶1.2](https://timsong-cpp.github.io/cppwp/std23/foo.bar#1.2)*',
            standard_ref('§[foo.bar]¶1.2'))
        self.assertEqual(
            '*[§[foo]¶note-1](https://timsong-cpp.github.io/cppwp/std23/foo#note-1)*',
            standard_ref('§[foo]¶note-1'))

    def test_doesnt_include_too_much(self):
        self.assertEqual(
            '*[§[foo.bar]¶1](https://timsong-cpp.github.io/cppwp/std23/foo.bar#1)*.', standard_ref('§[foo.bar]¶1.'))

    def test_doesnt_try_to_format_numbered_references(self):
        self.assertEqual('§1.2.3', standard_ref('§1.2.3'))
        self.assertEqual('§1.2.3¶1', standard_ref('§1.2.3¶1'))

    def test_given_multiple_paragraphs(self):
        self.assertEqual(
            '*[§[foo]](https://timsong-cpp.github.io/cppwp/std23/foo)*'
            '*[§[bar]](https://timsong-cpp.github.io/cppwp/std23/bar)*',
            standard_ref('§[foo]§[bar]'))
