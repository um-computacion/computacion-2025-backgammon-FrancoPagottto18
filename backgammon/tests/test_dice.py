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


    @patch("backgammon.core.dice.random.randint", side_effect=[3, 5])
    def test_tirar_normal(self, _mock_randint):
        d = Dice()
        valores = d.tirar()
        self.assertEqual(valores, [3, 5])
        self.assertEqual(d.get_dado1(), 3)
        self.assertEqual(d.get_dado2(), 5)
        self.assertFalse(d.es_doble())
        self.assertEqual(d.get_valores(), [3, 5])
     
    @patch("backgammon.core.dice.random.randint", side_effect=[4, 4])
    def test_tirar_doble(self, _mock_randint):
        d = Dice()
        valores = d.tirar()
        self.assertEqual(valores, [4, 4, 4, 4])
        self.assertEqual(d.get_dado1(), 4)
        self.assertEqual(d.get_dado2(), 4)
        self.assertTrue(d.es_doble())
        self.assertEqual(d.get_valores(), [4, 4, 4, 4])

    def test_repr(self):
        d = Dice()
        rep = repr(d)
        self.assertIn("Dice(0, 0, doble=False)", rep)


if __name__ == "__main__":
    unittest.main()