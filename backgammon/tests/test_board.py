import unittest
from backgammon.core.board import Board
class TestBoard(unittest.TestCase):
    def test_inicializacion_estandar(self):
        b = Board()
        puntos = b.get_puntos()
        # Blancas
        self.assertEqual(len(puntos[23]), 2)
        self.assertEqual(len(puntos[12]), 5)
        self.assertEqual(len(puntos[7]), 3)
        self.assertEqual(len(puntos[5]), 5)
        # Negras
        self.assertEqual(len(puntos[0]), 2)
        self.assertEqual(len(puntos[11]), 5)
        self.assertEqual(len(puntos[16]), 3)
        self.assertEqual(len(puntos[18]), 5)

    