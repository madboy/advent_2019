import unittest
from src import tools


class ToolsTest(unittest.TestCase):
    def test_get_digits_all(self):
        numbers = [1, 21, 340, 1234, 19002]
        expected = [
            (1, 0, 0, 0),
            (1, 2, 0, 0),
            (0, 4, 3, 0),
            (4, 3, 2, 1),
            (2, 0, 0, 9),
        ]
        for n, e in zip(numbers, expected):
            r = tools.get_digits(n)
            self.assertEqual(e, r)
