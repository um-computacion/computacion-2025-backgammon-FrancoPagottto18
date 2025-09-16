import unittest
from backgammon.core.Player import Player

class TestPlayer(unittest.TestCase):
    def test_init_correctamente(self):
        player = Player("Juan", "blanco")
        self.assertEqual(player.get_name(), "Juan")
        self.assertEqual(player.get_color(), "blanco")

