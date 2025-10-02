import unittest
from unittest.mock import patch

from backgammon.core.game import Game
from backgammon.core.exceptions import GameError, MovimientoInvalidoError, JuegoTerminadoError


class TestGame(unittest.TestCase):
    
    def test_inicializacion_correcta(self):
        """Test de inicialización del juego con nombres válidos"""
        game = Game("Alice", "Bob")
        self.assertEqual(game.get_player1().get_name(), "Colo)
        self.assertEqual(game.get_player1().get_color(), "blanco")
        self.assertEqual(game.get_player2().get_name(), "Juan")
        self.assertEqual(game.get_player2().get_color(), "negro")
        self.assertEqual(game.get_turno_actual(), game.get_player1())
        self.assertFalse(game.juego_terminado())
        self.assertIsNone(game.get_ganador())
    
    def test_inicializacion_nombres_vacios(self):
        """Test que falla con nombres vacíos"""
        with self.assertRaises(ValueError):
            Game("", "Juan")
        with self.assertRaises(ValueError):
            Game("Alice", "")
        with self.assertRaises(ValueError):
            Game("", "")
    
    def test_inicializacion_nombres_iguales(self):
        """Test que falla con nombres iguales"""
        with self.assertRaises(ValueError):
            Game("Colo", "Colo")
    
    def test_getters_basicos(self):
        """Test de todos los getters básicos"""
        game = Game("Colo", "Juan")
        
        # Test getters
        self.assertIsNotNone(game.get_board())
        self.assertIsNotNone(game.get_dice())
        self.assertEqual(game.get_player1().get_name(), "Colo")
        self.assertEqual(game.get_player2().get_name(), "Bob")
        self.assertEqual(game.get_turno_actual(), game.get_player1())
    
    def test_cambiar_turno(self):
        """Test de cambio de turnos"""
        game = Game("Colo", "Juan")
        
        # Inicialmente es el turno del jugador 1
        self.assertEqual(game.get_turno_actual(), game.get_player1())
        
        # Cambiar turno
        game.cambiar_turno()
        self.assertEqual(game.get_turno_actual(), game.get_player2())
        
        # Cambiar turno otra vez
        game.cambiar_turno()
        self.assertEqual(game.get_turno_actual(), game.get_player1())
    
    @patch("backgammon.core.dice.random.randint", side_effect=[3, 5])
    def test_tirar_dados_normal(self, _mock_randint):
        """Test de tirar dados con valores normales"""
        game = Game("Colo", "Juan")
        valores = game.tirar_dados()
        self.assertEqual(valores, [3, 5])
        self.assertEqual(game.get_dice().get_dado1(), 3)
        self.assertEqual(game.get_dice().get_dado2(), 5)
        self.assertFalse(game.get_dice().es_doble())
    
    @patch("backgammon.core.dice.random.randint", side_effect=[4, 4])
    def test_tirar_dados_doble(self, _mock_randint):
        """Test de tirar dados con doble"""
        game = Game("Colo", "Juan")
        valores = game.tirar_dados()
        self.assertEqual(valores, [4, 4, 4, 4])
        self.assertEqual(game.get_dice().get_dado1(), 4)
        self.assertEqual(game.get_dice().get_dado2(), 4)
        self.assertTrue(game.get_dice().es_doble())