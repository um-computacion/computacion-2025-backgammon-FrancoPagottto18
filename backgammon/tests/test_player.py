import unittest
from backgammon.core.Player import Player

class TestPlayer(unittest.TestCase):
    def test_init_correctamente(self):
        player = Player("Juan", "blanco")
        self.assertEqual(player.get_name(), "Juan")
        self.assertEqual(player.get_color(), "blanco")

    def test_get_name_(self):
        player = Player("María", "blanco")
        self.assertEqual(player.get_name(), "María")

    def test_get_color_(self):
        player = Player("Pedro", "negro")
        self.assertEqual(player.get_color(), "negro")

    def test_diferentes_colores(self):
        player_blanco = Player("Ana", "blanco")
        player_negro = Player("Carlos", "negro")
        self.assertEqual(player_blanco.get_color(), "blanco")
        self.assertEqual(player_negro.get_color(), "negro")

if __name__ == "__main__":
    unittest.main()

