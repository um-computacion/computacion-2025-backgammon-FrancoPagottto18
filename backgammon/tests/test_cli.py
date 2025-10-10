import unittest
from unittest.mock import patch, MagicMock, call
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

from backgammon.cli.main import BackgammonCLI
from backgammon.core.game import Game
from backgammon.core.exceptions import MovimientoInvalidoError, JuegoTerminadoError


class TestBackgammonCLI(unittest.TestCase):
    """Tests completos para BackgammonCLI"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.cli = BackgammonCLI()
    
    def tearDown(self):
        """Limpieza después de cada test"""
        self.cli = None
    
    def test_inicializacion(self):
        """Test de inicialización del CLI"""
        self.assertIsNone(self.cli.__game__)
        self.assertTrue(self.cli.__running__)
        self.assertEqual(self.cli.__dados_disponibles__, [])
        self.assertEqual(self.cli.__dados_usados__, [])
    
    @patch('builtins.input', side_effect=['nueva', 'Colo', 'Juan', 'salir'])
    @patch('builtins.print')
    def test_mostrar_inicio(self, mock_print, mock_input):
        """Test del mensaje de inicio"""
        self.cli._mostrar_inicio()
        
        # Verificar que se muestran los mensajes de inicio
        self.assertTrue(any("BACKGAMMON" in str(call) for call in mock_print.call_args_list))
        self.assertTrue(any("Objetivo: Llevar todas las fichas a casa" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['Colo', 'Juan'])
    def test_nueva_partida(self, mock_input):
        """Test de creación de nueva partida"""
        self.cli._nueva_partida()
        
        # Verificar que se creó el juego
        self.assertIsNotNone(self.cli.__game__)
        self.assertIsInstance(self.cli.__game__, Game)
        
        # Verificar que se limpiaron los dados
        self.assertEqual(self.cli.__dados_disponibles__, [])
        self.assertEqual(self.cli.__dados_usados__, [])
        
        # Verificar que se configuraron los jugadores
        self.assertEqual(self.cli.__game__.get_player1().get_name(), "Colo")
        self.assertEqual(self.cli.__game__.get_player2().get_name(), "Juan")
    
    @patch('builtins.input', side_effect=['', 'Juan'])
    def test_nueva_partida_nombre_vacio(self, mock_input):
        """Test que falla con nombre vacío"""
        with patch('builtins.print') as mock_print:
            self.cli._nueva_partida()
            
            # Verificar que se muestra error
            self.assertTrue(any("❌" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['Colo', 'Colo'])
    def test_nueva_partida_nombres_iguales(self, mock_input):
        """Test que falla con nombres iguales"""
        with patch('builtins.print') as mock_print:
            self.cli._nueva_partida()
            
            # Verificar que se muestra error
            self.assertTrue(any("❌" in str(call) for call in mock_print.call_args_list))
    
    def test_tirar_dados_sin_partida(self):
        """Test que falla al tirar dados sin partida"""
        with patch('builtins.print') as mock_print:
            self.cli._tirar_dados()
            
            # Verificar mensaje de error
            self.assertTrue(any("No hay partida" in str(call) for call in mock_print.call_args_list))
    
    def test_tirar_dados_con_partida(self):
        """Test de tirar dados con partida activa"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        
        with patch.object(self.cli.__game__, 'tirar_dados', return_value=[3, 5]) as mock_tirar:
            with patch.object(self.cli.__game__.get_dice(), 'es_doble', return_value=False):
                with patch('builtins.print') as mock_print:
                    self.cli._tirar_dados()
                    
                    # Verificar que se tiraron los dados
                    mock_tirar.assert_called_once()
                    
                    # Verificar que se almacenaron los dados
                    self.assertEqual(self.cli.__dados_disponibles__, [3, 5])
                    self.assertEqual(self.cli.__dados_usados__, [])
                    
                    # Verificar mensajes
                    self.assertTrue(any("Dados: [3, 5]" in str(call) for call in mock_print.call_args_list))
                    self.assertTrue(any("Dados disponibles: [3, 5]" in str(call) for call in mock_print.call_args_list))
    
    def test_tirar_dados_doble(self):
        """Test de tirar dados dobles"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        
        with patch.object(self.cli.__game__, 'tirar_dados', return_value=[4, 4, 4, 4]) as mock_tirar:
            with patch.object(self.cli.__game__.get_dice(), 'es_doble', return_value=True):
                with patch('builtins.print') as mock_print:
                    self.cli._tirar_dados()
                    
                    # Verificar que se almacenaron los dados dobles
                    self.assertEqual(self.cli.__dados_disponibles__, [4, 4, 4, 4])
                    
                    # Verificar mensaje de doble
                    self.assertTrue(any("¡Doble!" in str(call) for call in mock_print.call_args_list))
    
    def test_mover_ficha_sin_partida(self):
        """Test que falla al mover sin partida"""
        with patch('builtins.print') as mock_print:
            self.cli._mover_ficha()
            
            # Verificar mensaje de error
            self.assertTrue(any("No hay partida" in str(call) for call in mock_print.call_args_list))
    
    def test_mover_ficha_sin_dados(self):
        """Test que falla al mover sin dados"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        
        with patch('builtins.print') as mock_print:
            self.cli._mover_ficha()
            
            # Verificar mensaje de error
            self.assertTrue(any("No hay dados disponibles" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_valido(self, mock_input):
        """Test de movimiento válido"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch.object(self.cli.__game__, 'mover_ficha') as mock_mover:
            with patch('builtins.print') as mock_print:
                self.cli._mover_ficha()
                
                # Verificar que se llamó mover_ficha con índices correctos
                mock_mover.assert_called_once_with(0, 3)  # 1-1=0, 4-1=3
                
                # Verificar que se usó el dado correcto
                self.assertEqual(self.cli.__dados_disponibles__, [5])
                self.assertEqual(self.cli.__dados_usados__, [3])
                
                # Verificar mensaje de éxito
                self.assertTrue(any("Ficha movida" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['1', '7'])
    def test_mover_ficha_distancia_incorrecta(self, mock_input):
        """Test que falla con distancia incorrecta"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch('builtins.print') as mock_print:
            self.cli._mover_ficha()
            
            # Verificar mensaje de error
            self.assertTrue(any("distancia 6 no coincide" in str(call) for call in mock_print.call_args_list))
            
            # Verificar que no se usaron dados
            self.assertEqual(self.cli.__dados_disponibles__, [3, 5])
            self.assertEqual(self.cli.__dados_usados__, [])
    
    @patch('builtins.input', side_effect=['-1', '6'])
    def test_mover_ficha_desde_barra(self, mock_input):
        """Test de movimiento desde barra"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [6, 5]
        
        with patch.object(self.cli.__game__, 'mover_ficha') as mock_mover:
            with patch('builtins.print') as mock_print:
                self.cli._mover_ficha()
                
                # Verificar que se llamó mover_ficha desde barra
                mock_mover.assert_called_once_with(-1, 5)  # -1, 6-1=5
                
                # Verificar que se usó el dado correcto
                self.assertEqual(self.cli.__dados_disponibles__, [5])
                self.assertEqual(self.cli.__dados_usados__, [6])
    
    @patch('builtins.input', side_effect=['1', '-1'])
    def test_mover_ficha_bear_off(self, mock_input):
        """Test de bear off (sacar ficha)"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [24, 5]
        
        with patch.object(self.cli.__game__, 'mover_ficha') as mock_mover:
            with patch('builtins.print') as mock_print:
                self.cli._mover_ficha()
                
                # Verificar que se llamó mover_ficha para bear off
                mock_mover.assert_called_once_with(0, -1)  # 1-1=0, -1
                
                # Verificar que se usó el dado correcto
                self.assertEqual(self.cli.__dados_disponibles__, [5])
                self.assertEqual(self.cli.__dados_usados__, [24])
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_todos_dados_usados(self, mock_input):
        """Test cuando se usan todos los dados"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3]
        
        with patch.object(self.cli.__game__, 'mover_ficha'):
            with patch('builtins.print') as mock_print:
                self.cli._mover_ficha()
                
                # Verificar que se acabaron los dados
                self.assertEqual(self.cli.__dados_disponibles__, [])
                self.assertEqual(self.cli.__dados_usados__, [3])
                
                # Verificar mensaje de turno completo
                self.assertTrue(any("Todos los dados utilizados" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_juego_terminado(self, mock_input):
        """Test cuando el juego termina después del movimiento"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        # Simular juego terminado
        with patch.object(self.cli.__game__, 'juego_terminado', return_value=True):
            with patch.object(self.cli.__game__, 'get_ganador', return_value=self.cli.__game__.get_player1()):
                with patch.object(self.cli.__game__, 'mover_ficha'):
                    with patch('builtins.print') as mock_print:
                        self.cli._mover_ficha()
                        
                        # Verificar mensaje de juego terminado
                        self.assertTrue(any("JUEGO TERMINADO" in str(call) for call in mock_print.call_args_list))
    
    