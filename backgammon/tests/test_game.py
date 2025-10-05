import unittest
from unittest.mock import patch

from backgammon.core.game import Game
from backgammon.core.exceptions import GameError, MovimientoInvalidoError, JuegoTerminadoError


class TestGame(unittest.TestCase):
    
    def test_inicializacion_correcta(self):
        """Test de inicialización del juego con nombres válidos"""
        game = Game("Colo", "Juan")
        self.assertEqual(game.get_player1().get_name(), "Colo")
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
            Game("Colo", "")
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
        self.assertEqual(game.get_player2().get_name(), "Juan")
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

     def test_tirar_dados_juego_terminado(self):
        """Test que no se pueden tirar dados en juego terminado"""
        game = Game("Colo", "Juan")
        game.__juego_terminado__ = True
        
        with self.assertRaises(JuegoTerminadoError):
            game.tirar_dados()
    
    def test_mover_ficha_valido(self):
        """Test de movimiento válido de ficha"""
        game = Game("Colo", "Juan")
        
        # Mover ficha blanca del punto 5 al punto 4 (punto 5 tiene fichas blancas)
        game.mover_ficha(5, 4)
        
        # Verificar que se movió correctamente
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[5]), 4)  # Quedaron 4 fichas en punto 5 (tenía 5)
        self.assertEqual(len(puntos[4]), 1)  # Hay 1 ficha en punto 4
        self.assertEqual(puntos[4][0].get_color(), "blanco")
    
    def test_mover_ficha_desde_barra(self):
        """Test de reintroducir ficha desde la barra"""
        game = Game("Colo", "Juan")
        
        # Primero poner una ficha en la barra
        game.get_board().agregar_barra("blanco")
        
        # Reintroducir desde la barra al punto 6 (punto vacío)
        game.mover_ficha(-1, 6)
        
        # Verificar que se reintrodujo
        self.assertEqual(len(game.get_board().get_barra()["blanco"]), 0)
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[6]), 1)  # 1 ficha reintroducida
    
    def test_mover_ficha_invalido_mismo_punto(self):
        """Test que falla al mover al mismo punto"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError):
            game.mover_ficha(0, 0)
    
    def test_mover_ficha_invalido_punto_vacio(self):
        """Test que falla al mover desde punto vacío"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError):
            game.mover_ficha(10, 11)  # Punto 10 está vacío inicialmente
    
    def test_mover_ficha_invalido_color_incorrecto(self):
        """Test que falla al mover ficha del oponente"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError):
            game.mover_ficha(0, 1)  # Punto 0 tiene fichas negras, pero es turno de blanco
    
    def test_mover_ficha_comer_ficha(self):
        """Test de comer ficha del oponente"""
        game = Game("Colo", "Juan")
        
        # Poner una ficha negra en punto 4 (punto vacío)
        game.get_board().agregar_ficha("negro", 4)
        
        # Mover ficha blanca del punto 5 al punto 4 (comer)
        game.mover_ficha(5, 4)
        
        # Verificar que se comió la ficha
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[4]), 1)
        self.assertEqual(puntos[4][0].get_color(), "blanco")
        
        # Verificar que la ficha negra está en la barra
        self.assertEqual(len(game.get_board().get_barra()["negro"]), 1)
        
    def test_mover_ficha_bloqueado(self):
        """Test que falla al mover a punto bloqueado"""
        game = Game("Colo", "Juan")
        
        # Poner 2 fichas negras en punto 4 (bloqueado)
        game.get_board().agregar_ficha("negro", 4)
        game.get_board().agregar_ficha("negro", 4)
        
        with self.assertRaises(MovimientoInvalidoError):
            game.mover_ficha(5, 4)  # No se puede mover a punto bloqueado
    
    def test_mover_ficha_juego_terminado(self):
        """Test que no se pueden hacer movimientos en juego terminado"""
        game = Game("Colo", "Juan")
        game.__juego_terminado__ = True
        
        with self.assertRaises(JuegoTerminadoError):
            game.mover_ficha(0, 1)
    
    def test_verificar_ganador_sin_ganador(self):
        """Test de verificación de ganador cuando no hay ganador"""
        game = Game("Colo", "Juan")
        ganador = game.verificar_ganador()
        self.assertIsNone(ganador)
        self.assertFalse(game.juego_terminado())
    
    def test_verificar_ganador_jugador_blanco(self):
        """Test de verificación de ganador - jugador blanco gana"""
        game = Game("Colo", "Juan")
        
        # Simular que el jugador blanco tiene todas las fichas en casa
        # Limpiar el tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        
        # Poner 15 fichas blancas en casa (puntos 18-23)
        for i in range(18, 24):
            for _ in range(3):  # 3 fichas por punto = 18 fichas
                game.get_board().agregar_ficha("blanco", i)
        
        # Ajustar para tener exactamente 15 fichas (quitar 3 fichas extra)
        for _ in range(3):
            game.get_board().quitar_ficha(18)
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player1())
        self.assertTrue(game.juego_terminado())
        self.assertEqual(game.get_ganador(), game.get_player1())
    
    def test_verificar_ganador_jugador_negro(self):
        """Test de verificación de ganador - jugador negro gana"""
        game = Game("Colo", "Juan")
        
        # Simular que el jugador negro tiene todas las fichas en casa
        # Limpiar el tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        
        # Poner 15 fichas negras en casa (puntos 0-5)
        for i in range(6):
            for _ in range(3):  # 3 fichas por punto = 18 fichas
                game.get_board().agregar_ficha("negro", i)
        
        # Ajustar para tener exactamente 15 fichas (quitar 3 fichas extra)
        for _ in range(3):
            game.get_board().quitar_ficha(0)
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player2())
        self.assertTrue(game.juego_terminado())
        self.assertEqual(game.get_ganador(), game.get_player2())
    
    def test_reiniciar_juego(self):
        """Test de reinicio del juego"""
        game = Game("Colo", "Juan")
        
        # Modificar el estado del juego
        game.cambiar_turno()
        game.__juego_terminado__ = True
        game.__ganador__ = game.get_player1()
        
        # Reiniciar
        game.reiniciar_juego()
        
        # Verificar que se reinició correctamente
        self.assertEqual(game.get_turno_actual(), game.get_player1())
        self.assertFalse(game.juego_terminado())
        self.assertIsNone(game.get_ganador())
        
        # Verificar que el tablero se reinició
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[0]), 2)  # Configuración inicial
        self.assertEqual(len(puntos[23]), 2)  # Configuración inicial


if __name__ == "__main__":
    unittest.main()

    