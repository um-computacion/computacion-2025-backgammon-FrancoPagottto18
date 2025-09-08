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
    def test_agregar_ficha_en_punto(self):
        b = Board()
        b.agregar_ficha("blanco", 1)
        self.assertEqual(len(b.get_puntos()[1]), 1)

    def test_quitar_ficha_en_punto(self):
        b = Board()
        b.agregar_ficha("blanco", 1)
        ok = b.quitar_ficha(1)
        self.assertTrue(ok)
        self.assertEqual(len(b.get_puntos()[1]), 0)
        self.assertFalse(b.quitar_ficha(1))

    