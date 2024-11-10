import unittest

from quiz.formatting import format


class FormatTest(unittest.TestCase):
    def test_format(self):
        unformatted = """
        int main() { return 0;
        }
        """
        formatted = "\nint main() { return 0; }\n"
        self.assertEqual(formatted, format(unformatted))
