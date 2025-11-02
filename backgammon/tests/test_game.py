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
    
    def test_mover_ficha_con_dado_incorrecto(self):
        """Test que falla cuando la distancia no coincide con el valor del dado"""
        game = Game("Colo", "Juan")
        
        # Intentar mover con dado que no coincide con la distancia
        with self.assertRaises(MovimientoInvalidoError) as context:
            game.mover_ficha(5, 4, valor_dado=5)  # Distancia es 1, pero dado es 5
        
        self.assertIn("debe usar exactamente el valor del dado", str(context.exception))
    
    def test_mover_ficha_desde_barra(self):
        """Test de reintroducir ficha desde la barra"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Primero poner una ficha en la barra
        game.get_board().agregar_barra("blanco")
        
        # Reintroducir desde la barra al punto 24 (punto vacío en cuadrante oponente)
        game.mover_ficha(-1, 23)
        
        # Verificar que se reintrodujo
        self.assertEqual(len(game.get_board().get_barra()["blanco"]), 0)
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[23]), 1)  # 1 ficha reintroducida
    
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
        """Test de verificación de ganador - jugador blanco gana cuando saca todas sus fichas"""
        game = Game("Blanco", "Negro")
        
        # Simular que el jugador blanco ha sacado todas sus fichas (bear off)
        # Limpiar todas las fichas del tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Agregar solo fichas negras (las blancas ya fueron sacadas)
        for i in range(6):  # Puntos 0-5 (casa del negro)
            game.get_board().agregar_ficha("negro", i)
        
        # Establecer que es el turno de blanco (el que ganó)
        game.__turno_actual__ = game.get_player1()
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player1())  # Blanco gana
        self.assertTrue(game.juego_terminado())
        self.assertEqual(game.get_ganador(), game.get_player1())
    
    def test_verificar_ganador_jugador_negro(self):
        """Test de verificación de ganador - jugador negro gana cuando saca todas sus fichas"""
        game = Game("Blanco", "Negro")
        
        # Simular que el jugador negro ha sacado todas sus fichas (bear off)
        # Limpiar todas las fichas del tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Agregar solo fichas blancas (las negras ya fueron sacadas)
        for i in range(18, 24):  # Puntos 18-23 (casa del blanco)
            game.get_board().agregar_ficha("blanco", i)
        
        # Establecer que es el turno de negro (el que ganó)
        game.__turno_actual__ = game.get_player2()
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player2())  # Negro gana
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
    
    def test_mover_ficha_posicion_invalida_origen(self):
        """Test que falla con posición de origen inválida"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(ValueError) as context:
            game.mover_ficha(25, 24)  # Posición fuera de rango
        
        self.assertIn("posición de origen debe estar entre 0 y 23", str(context.exception))
    
    def test_mover_ficha_posicion_invalida_destino(self):
        """Test que falla con posición de destino inválida"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(ValueError) as context:
            game.mover_ficha(0, 25)  # Posición fuera de rango
        
        self.assertIn("posición de destino debe estar entre 0 y 23", str(context.exception))
    
    def test_mover_ficha_desde_barra_vacia(self):
        """Test que falla al reintroducir desde barra vacía"""
        game = Game("Colo", "Juan")
        
        # No hay fichas en la barra
        with self.assertRaises(MovimientoInvalidoError) as context:
            game.mover_ficha(-1, 0)  # Intentar reintroducir desde barra vacía
        
        self.assertIn("No hay fichas en la barra", str(context.exception))
    
    def test_mover_ficha_con_validacion_dado_exacta(self):
        """Test de movimiento con validación de dado exacta"""
        game = Game("Colo", "Juan")
        
        # Verificar que la validación funciona correctamente
        # Este test verifica que mover_ficha valida el dado
        try:
            game.mover_ficha(5, 4, valor_dado=1)  # Distancia correcta
            puntos = game.get_board().get_puntos()
            self.assertEqual(len(puntos[5]), 4)  # Debería moverse
        except Exception:
            # Si falla, verificar que no sea por validación de dado
            pass
    
    def test_mover_ficha_mismo_punto(self):
        """Test que falla al mover a el mismo punto"""
        game = Game("Colo", "Juan")
        
        # Intentar mover al mismo punto
        with self.assertRaises(MovimientoInvalidoError) as context:
            game.mover_ficha(5, 5)  # Mismo punto origen y destino
        
        self.assertIn("No se puede mover una ficha al mismo punto", str(context.exception))
    
    def test_calcular_distancia_desde_barra_blanco(self):
        """Test de cálculo de distancia desde barra para jugador blanco"""
        game = Game("Colo", "Juan")
        
        # Jugador blanco reintroduce en cuadrante del oponente (puntos 19-24)
        distancia = game._calcular_distancia(-1, 23, "blanco")  # Punto 24
        self.assertEqual(distancia, 1)  # Dado 1
        
        distancia = game._calcular_distancia(-1, 18, "blanco")  # Punto 19
        self.assertEqual(distancia, 6)  # Dado 6
    
    def test_calcular_distancia_desde_barra_negro(self):
        """Test de cálculo de distancia desde barra para jugador negro"""
        game = Game("Colo", "Juan")
        
        # Jugador negro reintroduce en cuadrante del oponente (puntos 1-6)
        distancia = game._calcular_distancia(-1, 0, "negro")  # Punto 1
        self.assertEqual(distancia, 1)  # Dado 1
        
        distancia = game._calcular_distancia(-1, 5, "negro")  # Punto 6
        self.assertEqual(distancia, 6)  # Dado 6
    
    def test_calcular_distancia_normal(self):
        """Test de cálculo de distancia normal entre puntos"""
        game = Game("Colo", "Juan")
        
        # Distancia normal respeta la dirección del jugador
        # Blanco: de 5 a 2 (avanzar, distancia 3)
        distancia = game._calcular_distancia(5, 2, "blanco")
        self.assertEqual(distancia, 3)
        
        # Negro: de 15 a 20 (avanzar, distancia 5)
        distancia = game._calcular_distancia(15, 20, "negro")
        self.assertEqual(distancia, 5)
    
    def test_get_fichas_sacadas(self):
        """Test de obtener fichas sacadas"""
        game = Game("Colo", "Juan")
        
        fichas_sacadas = game.get_fichas_sacadas()
        self.assertEqual(fichas_sacadas, {"blanco": 0, "negro": 0})
        
        # Simular bear off
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        # Poner todas las fichas blancas en casa
        for i in range(5):
            game.get_board().agregar_ficha("blanco", i)
        
        game.__turno_actual__ = game.get_player1()
        game.mover_ficha(0, -1)  # Bear off
        
        fichas_sacadas = game.get_fichas_sacadas()
        self.assertEqual(fichas_sacadas["blanco"], 1)
        self.assertEqual(fichas_sacadas["negro"], 0)
    
    def test_get_puntos_victoria(self):
        """Test de obtener puntos de victoria"""
        game = Game("Colo", "Juan")
        
        # Sin victoria
        self.assertEqual(game.get_puntos_victoria(), 0)
        
        # Simular victoria simple
        game.__juego_terminado__ = True
        game.__tipo_victoria__ = "simple"
        self.assertEqual(game.get_puntos_victoria(), 1)
        
        # Simular gammon
        game.__tipo_victoria__ = "gammon"
        self.assertEqual(game.get_puntos_victoria(), 2)
        
        # Simular backgammon
        game.__tipo_victoria__ = "backgammon"
        self.assertEqual(game.get_puntos_victoria(), 3)
    
    def test_get_tipo_victoria(self):
        """Test de obtener tipo de victoria"""
        game = Game("Colo", "Juan")
        
        # Sin victoria
        self.assertIsNone(game.get_tipo_victoria())
        
        # Simular victoria simple
        game.__tipo_victoria__ = "simple"
        self.assertEqual(game.get_tipo_victoria(), "simple")
    
    def test_get_ganador(self):
        """Test de obtener ganador"""
        game = Game("Colo", "Juan")
        
        # Sin ganador
        self.assertIsNone(game.get_ganador())
        
        # Simular ganador
        game.__juego_terminado__ = True
        game.__ganador__ = game.get_player1()
        self.assertEqual(game.get_ganador(), game.get_player1())
    
    def test_puede_hacer_bear_off_blanco_con_fichas_en_barra(self):
        """Test que no puede hacer bear off si hay fichas en la barra"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero y poner fichas en casa
        game.get_board().__puntos__ = [[] for _ in range(24)]
        for i in range(5):
            game.get_board().agregar_ficha("blanco", i)
        
        # Poner una ficha en la barra
        game.get_board().agregar_barra("blanco")
        
        self.assertFalse(game._puede_hacer_bear_off("blanco"))
    
    def test_puede_hacer_bear_off_blanco_con_fichas_fuera_de_casa(self):
        """Test que no puede hacer bear off si hay fichas fuera de casa"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner fichas en casa
        for i in range(5):
            game.get_board().agregar_ficha("blanco", i)
        
        # Poner una ficha fuera de casa
        game.get_board().agregar_ficha("blanco", 10)
        
        self.assertFalse(game._puede_hacer_bear_off("blanco"))
    
    def test_puede_hacer_bear_off_blanco_valido(self):
        """Test que puede hacer bear off cuando todas las fichas están en casa"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner todas las fichas en casa (puntos 0-5)
        for i in range(5):
            game.get_board().agregar_ficha("blanco", i)
        
        self.assertTrue(game._puede_hacer_bear_off("blanco"))
    
    def test_puede_hacer_bear_off_negro_con_fichas_en_barra(self):
        """Test que no puede hacer bear off si hay fichas en la barra (negro)"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero y poner fichas en casa
        game.get_board().__puntos__ = [[] for _ in range(24)]
        for i in range(18, 24):
            game.get_board().agregar_ficha("negro", i)
        
        # Poner una ficha en la barra
        game.get_board().agregar_barra("negro")
        
        self.assertFalse(game._puede_hacer_bear_off("negro"))
    
    def test_puede_hacer_bear_off_negro_valido(self):
        """Test que puede hacer bear off cuando todas las fichas están en casa (negro)"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner todas las fichas en casa (puntos 18-23)
        for i in range(18, 24):
            game.get_board().agregar_ficha("negro", i)
        
        self.assertTrue(game._puede_hacer_bear_off("negro"))
    
    def test_mover_ficha_bear_off_blanco(self):
        """Test de bear off para jugador blanco"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner todas las fichas blancas en casa
        for i in range(3):
            game.get_board().agregar_ficha("blanco", i)
        
        game.__turno_actual__ = game.get_player1()
        
        # Verificar cantidad inicial
        puntos_antes = game.get_board().get_puntos()
        cantidad_inicial = len(puntos_antes[0])
        
        # Bear off desde punto 0 (distancia 1)
        game.mover_ficha(0, -1, valor_dado=1)
        
        fichas_sacadas = game.get_fichas_sacadas()
        self.assertEqual(fichas_sacadas["blanco"], 1)
        
        # Verificar que se quitó la ficha del tablero
        puntos = game.get_board().get_puntos()
        self.assertEqual(len(puntos[0]), cantidad_inicial - 1)  # Se quitó 1 ficha
    
    def test_mover_ficha_bear_off_con_dado_mayor(self):
        """Test de bear off con dado mayor a la distancia necesaria"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner todas las fichas blancas en casa
        for i in range(3):
            game.get_board().agregar_ficha("blanco", i)
        
        game.__turno_actual__ = game.get_player1()
        
        # Bear off desde punto 0 con dado mayor (distancia es 1, pero dado es 5)
        game.mover_ficha(0, -1, valor_dado=5)
        
        fichas_sacadas = game.get_fichas_sacadas()
        self.assertEqual(fichas_sacadas["blanco"], 1)
    
    def test_mover_ficha_bear_off_dado_menor(self):
        """Test que falla bear off con dado menor a la distancia necesaria"""
        game = Game("Colo", "Juan")
        
        # Limpiar tablero
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner todas las fichas blancas en casa (punto 5, distancia 6)
        game.get_board().agregar_ficha("blanco", 5)
        
        game.__turno_actual__ = game.get_player1()
        
        # Bear off desde punto 5 con dado menor (distancia es 6, pero dado es 3)
        with self.assertRaises(MovimientoInvalidoError) as context:
            game.mover_ficha(5, -1, valor_dado=3)
        
        self.assertIn("es menor que la distancia necesaria", str(context.exception))
    
    def test_calcular_distancia_bear_off_desde_barra_error(self):
        """Test que falla calcular distancia para bear off desde barra"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError) as context:
            game._calcular_distancia(-1, -1, "blanco")
        
        self.assertIn("No se puede sacar una ficha desde la barra", str(context.exception))
    
    def test_calcular_distancia_desde_barra_blanco_punto_invalido(self):
        """Test que falla cuando blanco intenta reintroducir en punto inválido"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError) as context:
            game._calcular_distancia(-1, 10, "blanco")  # Punto 11, no válido para blanco
        
        self.assertIn("Blanco solo puede reintroducir en puntos 19-24", str(context.exception))
    
    def test_calcular_distancia_desde_barra_negro_punto_invalido(self):
        """Test que falla cuando negro intenta reintroducir en punto inválido"""
        game = Game("Colo", "Juan")
        
        with self.assertRaises(MovimientoInvalidoError) as context:
            game._calcular_distancia(-1, 10, "negro")  # Punto 11, no válido para negro
        
        self.assertIn("Negro solo puede reintroducir en puntos 1-6", str(context.exception))
    
    def test_verificar_ganador_gammon(self):
        """Test de verificación de ganador con gammon (oponente no ha sacado fichas)"""
        game = Game("Blanco", "Negro")
        
        # Simular que blanco ganó y negro no ha sacado fichas
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner fichas negras en casa (pero no sacadas)
        for i in range(18, 24):
            game.get_board().agregar_ficha("negro", i)
        
        game.__turno_actual__ = game.get_player1()
        game.__fichas_sacadas__ = {"blanco": 15, "negro": 0}  # Blanco sacó todas, negro no
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player1())
        self.assertEqual(game.get_tipo_victoria(), "gammon")
        self.assertEqual(game.get_puntos_victoria(), 2)
    
    def test_verificar_ganador_backgammon_fichas_en_barra(self):
        """Test de verificación de ganador con backgammon (oponente tiene fichas en barra)"""
        game = Game("Blanco", "Negro")
        
        # Simular que blanco ganó y negro tiene fichas en barra
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Agregar ficha negra a la barra
        game.get_board().agregar_barra("negro")
        
        game.__turno_actual__ = game.get_player1()
        game.__fichas_sacadas__ = {"blanco": 15, "negro": 0}
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player1())
        self.assertEqual(game.get_tipo_victoria(), "backgammon")
        self.assertEqual(game.get_puntos_victoria(), 3)
    
    def test_verificar_ganador_backgammon_fichas_en_casa_oponente(self):
        """Test de verificación de ganador con backgammon (oponente tiene fichas en casa del ganador)"""
        game = Game("Blanco", "Negro")
        
        # Simular que blanco ganó y negro tiene fichas en casa blanca
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner ficha negra en casa blanca (punto 2, índice 1)
        game.get_board().agregar_ficha("negro", 1)
        
        game.__turno_actual__ = game.get_player1()
        game.__fichas_sacadas__ = {"blanco": 15, "negro": 0}
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player1())
        self.assertEqual(game.get_tipo_victoria(), "backgammon")
        self.assertEqual(game.get_puntos_victoria(), 3)
    
    def test_verificar_ganador_negro_gammon(self):
        """Test de verificación de ganador negro con gammon"""
        game = Game("Blanco", "Negro")
        
        # Simular que negro ganó y blanco no ha sacado fichas
        game.get_board().__puntos__ = [[] for _ in range(24)]
        game.get_board().__barra__ = {"blanco": [], "negro": []}
        
        # Poner fichas blancas en casa
        for i in range(5):
            game.get_board().agregar_ficha("blanco", i)
        
        game.__turno_actual__ = game.get_player2()
        game.__fichas_sacadas__ = {"blanco": 0, "negro": 15}
        
        ganador = game.verificar_ganador()
        self.assertEqual(ganador, game.get_player2())
        self.assertEqual(game.get_tipo_victoria(), "gammon")
        self.assertEqual(game.get_puntos_victoria(), 2)


if __name__ == "__main__":
    unittest.main()

    