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

