import unittest
from unittest.mock import patch

from backgammon.core.dice import Dice

class TestDice(unittest.TestCase):
    def test_estado_inicial(self):
        d = Dice()
        self.assertEqual(d.get_dado1(), 0)
        self.assertEqual(d.get_dado2(), 0)
        self.assertFalse(d.es_doble())
        self.assertEqual(d.get_valores(), [0, 0])

