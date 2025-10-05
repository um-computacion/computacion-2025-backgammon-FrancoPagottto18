import unittest
from backgammon.core.checker import Checker

class TestChecker(unittest.TestCase):
    def test_get_color(self):
        c = Checker("blanco")
        self.assertEqual(c.get_color(), "blanco")

    def test_str(self):
        c = Checker("negro")
        self.assertEqual(str(c), "negro")

if __name__ == "__main__":
    unittest.main()