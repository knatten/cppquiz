import unittest

from quiz.management.commands.remove_section_numbers import remove_section_numbers


class TestRemoveSectionNumbers(unittest.TestCase):
    def test_no_section_numbers_is_unchanged(self):
        self.assertEqual("foo\nbar", remove_section_numbers("foo\nbar"))
        self.assertEqual("foo [expr.cond] bar", remove_section_numbers("foo [expr.cond] bar"))

    def test_replaces_section_numbers(self):
        self.assertEqual("foo §[expr.cond] bar", remove_section_numbers("foo [expr.cond]§8 bar"))
        self.assertEqual("foo §[expr.cond] bar", remove_section_numbers("foo [expr.cond]§10.20 bar"))
        self.assertEqual("foo §[expr.cond] bar", remove_section_numbers("foo [expr.cond]§1.2.3 bar"))
        self.assertEqual("foo §[expr.cond]¶wat bar", remove_section_numbers("foo [expr.cond]§1.2.3¶wat bar"))

    def test_doesnt_replace_too_much(self):
        self.assertEqual("[1] §[conv.ptr]¶1", remove_section_numbers("[1] [conv.ptr]§7.11¶1"))

    def test_bare_section_numbers_raises(self):
        with self.assertRaises(ValueError) as _:
            remove_section_numbers("foo §8 bar")

    def test_larger_text(self):
        original = """
        foo [aa.bb]§1.23¶2
        standard[aa.bb]§1.23¶2:
        """
        expected = """
        foo §[aa.bb]¶2
        standard§[aa.bb]¶2:
        """
        self.assertEqual(expected, remove_section_numbers(original))
