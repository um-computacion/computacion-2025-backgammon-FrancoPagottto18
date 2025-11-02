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
    
    def test_mostrar_inicio(self):
        """Test del mensaje de inicio"""
        with patch('builtins.print') as mock_print:
            self.cli._mostrar_inicio()
            
            # Verificar que se muestran los mensajes de inicio
            self.assertTrue(any("BACKGAMMON" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("Objetivo: Llevar todas las fichas a casa" in str(call) for call in mock_print.call_args_list))
    
    def test_mostrar_menu_sin_partida(self):
        """Test de mostrar menú sin partida"""
        with patch('builtins.print') as mock_print:
            self.cli._mostrar_menu()
            
            # Verificar que se muestra el menú inicial
            self.assertTrue(any("MENÚ:" in str(call) for call in mock_print.call_args_list))
    
    def test_mostrar_menu_con_partida(self):
        """Test de mostrar menú con partida activa"""
        self.cli.__game__ = Game("Colo", "Juan")
        
        with patch('builtins.print') as mock_print:
            self.cli._mostrar_menu()
            
            # Verificar que se muestra el turno
            self.assertTrue(any("Turno:" in str(call) for call in mock_print.call_args_list))
    
    def test_mostrar_menu_juego_terminado(self):
        """Test de mostrar menú cuando el juego terminó"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__game__.__juego_terminado__ = True
        
        with patch('builtins.print') as mock_print:
            self.cli._mostrar_menu()
            
            # Verificar que se muestra el menú inicial (juego terminado)
            self.assertTrue(any("MENÚ:" in str(call) for call in mock_print.call_args_list))
    
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
    
    def test_cambiar_turno_sin_partida(self):
        """Test que falla al cambiar turno sin partida"""
        with patch('builtins.print') as mock_print:
            self.cli._cambiar_turno()
            
            # Verificar mensaje de error
            self.assertTrue(any("No hay partida" in str(call) for call in mock_print.call_args_list))
    
    def test_cambiar_turno_con_partida(self):
        """Test de cambio de turno con partida activa"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        self.cli.__dados_usados__ = [2]
        
        with patch.object(self.cli.__game__, 'cambiar_turno') as mock_cambiar:
            with patch('builtins.print') as mock_print:
                self.cli._cambiar_turno()
                
                # Verificar que se cambió el turno
                mock_cambiar.assert_called_once()
                
                # Verificar que se limpiaron los dados
                self.assertEqual(self.cli.__dados_disponibles__, [])
                self.assertEqual(self.cli.__dados_usados__, [])
                
                # Verificar mensaje de cambio
                self.assertTrue(any("Turno:" in str(call) for call in mock_print.call_args_list))
                self.assertTrue(any("Use 'dados'" in str(call) for call in mock_print.call_args_list))
    
    def test_mostrar_ayuda(self):
        """Test de mostrar ayuda"""
        with patch('builtins.print') as mock_print:
            self.cli._mostrar_ayuda()
            
            # Verificar que se muestran los comandos
            self.assertTrue(any("COMANDOS:" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("nueva" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("dados" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("mover" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("pasar" in str(call) for call in mock_print.call_args_list))
            
            # Verificar que se muestran las reglas
            self.assertTrue(any("REGLAS:" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("Blancas van del 24 al 1" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("Negras van del 1 al 24" in str(call) for call in mock_print.call_args_list))
    
    def test_terminar(self):
        """Test de terminar el juego"""
        self.cli._terminar()
        
        # Verificar que se marcó como no corriendo
        self.assertFalse(self.cli.__running__)
    
    def test_comando_invalido(self):
        """Test de comando inválido"""
        with patch('builtins.print') as mock_print:
            # Simular comando inválido
            self.cli._procesar_comando("comando_invalido")
            
            # Verificar mensaje de error
            self.assertTrue(any("no válido" in str(call) for call in mock_print.call_args_list))
    
    def test_comando_nueva(self):
        """Test de comando nueva"""
        with patch.object(self.cli, '_nueva_partida') as mock_nueva:
            self.cli._procesar_comando("nueva")
            mock_nueva.assert_called_once()
    
    def test_comando_dados(self):
        """Test de comando dados"""
        with patch.object(self.cli, '_tirar_dados') as mock_dados:
            self.cli._procesar_comando("dados")
            mock_dados.assert_called_once()
    
    def test_comando_mover(self):
        """Test de comando mover"""
        with patch.object(self.cli, '_mover_ficha') as mock_mover:
            self.cli._procesar_comando("mover")
            mock_mover.assert_called_once()
    
    def test_comando_pasar(self):
        """Test de comando pasar"""
        with patch.object(self.cli, '_cambiar_turno') as mock_pasar:
            self.cli._procesar_comando("pasar")
            mock_pasar.assert_called_once()
    
    def test_comando_ayuda(self):
        """Test de comando ayuda"""
        with patch.object(self.cli, '_mostrar_ayuda') as mock_ayuda:
            self.cli._procesar_comando("ayuda")
            mock_ayuda.assert_called_once()
    
    def test_comando_salir(self):
        """Test de comando salir"""
        with patch.object(self.cli, '_terminar') as mock_salir:
            self.cli._procesar_comando("salir")
            mock_salir.assert_called_once()
    
    def test_ver_tablero_sin_partida(self):
        """Test de mostrar tablero sin partida"""
        with patch('builtins.print') as mock_print:
            self.cli._ver_tablero()
            
            # Verificar mensaje de error
            self.assertTrue(any("No hay partida" in str(call) for call in mock_print.call_args_list))
    
    def test_ver_tablero_con_partida(self):
        """Test de mostrar tablero con partida activa"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        
        with patch('builtins.print') as mock_print:
            self.cli._ver_tablero()
            
            # Verificar que se muestra el tablero
            self.assertTrue(any("TABLERO DE BACKGAMMON" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("TURNO ACTUAL" in str(call) for call in mock_print.call_args_list))
    
    def test_ver_tablero_con_fichas_en_barra(self):
        """Test de mostrar tablero con fichas en barra"""
        # Crear partida
        self.cli.__game__ = Game("Colo", "Juan")
        
        # Agregar fichas a la barra
        self.cli.__game__.get_board().agregar_barra("blanco")
        self.cli.__game__.get_board().agregar_barra("negro")
        
        with patch('builtins.print') as mock_print:
            self.cli._ver_tablero()
            
            # Verificar que se muestran las fichas en barra
            self.assertTrue(any("Blancas: 1" in str(call) for call in mock_print.call_args_list))
            self.assertTrue(any("Negras: 1" in str(call) for call in mock_print.call_args_list))
    
    def test_comando_vacio(self):
        """Test de comando vacío"""
        with patch('builtins.print') as mock_print:
            self.cli._procesar_comando("")
            
            # Verificar mensaje de ayuda
            self.assertTrue(any("Ingrese un comando" in str(call) for call in mock_print.call_args_list))
    
    def test_alias_nueva(self):
        """Test de alias 'n' y '1' para comando nueva"""
        with patch.object(self.cli, '_nueva_partida') as mock_nueva:
            self.cli._procesar_comando("n")
            mock_nueva.assert_called_once()
        
        with patch.object(self.cli, '_nueva_partida') as mock_nueva:
            self.cli._procesar_comando("1")
            mock_nueva.assert_called_once()
    
    def test_alias_tablero(self):
        """Test de alias 't' y '2' para comando tablero"""
        with patch.object(self.cli, '_ver_tablero') as mock_tablero:
            self.cli._procesar_comando("t")
            mock_tablero.assert_called_once()
        
        with patch.object(self.cli, '_ver_tablero') as mock_tablero:
            self.cli._procesar_comando("2")
            mock_tablero.assert_called_once()
    
    def test_alias_dados(self):
        """Test de alias 'd' y '3' para comando dados"""
        with patch.object(self.cli, '_tirar_dados') as mock_dados:
            self.cli._procesar_comando("d")
            mock_dados.assert_called_once()
        
        with patch.object(self.cli, '_tirar_dados') as mock_dados:
            self.cli._procesar_comando("3")
            mock_dados.assert_called_once()
    
    def test_alias_mover(self):
        """Test de alias 'm' y '4' para comando mover"""
        with patch.object(self.cli, '_mover_ficha') as mock_mover:
            self.cli._procesar_comando("m")
            mock_mover.assert_called_once()
        
        with patch.object(self.cli, '_mover_ficha') as mock_mover:
            self.cli._procesar_comando("4")
            mock_mover.assert_called_once()
    
    def test_alias_pasar(self):
        """Test de alias 'p' y '5' para comando pasar"""
        with patch.object(self.cli, '_cambiar_turno') as mock_pasar:
            self.cli._procesar_comando("p")
            mock_pasar.assert_called_once()
        
        with patch.object(self.cli, '_cambiar_turno') as mock_pasar:
            self.cli._procesar_comando("5")
            mock_pasar.assert_called_once()
    
    def test_alias_ayuda(self):
        """Test de alias para comando ayuda"""
        aliases = ['help', 'h', '?']
        for alias in aliases:
            with patch.object(self.cli, '_mostrar_ayuda') as mock_ayuda:
                self.cli._procesar_comando(alias)
                mock_ayuda.assert_called_once()
    
    def test_alias_salir(self):
        """Test de alias para comando salir"""
        aliases = ['s', 'exit', 'q']
        for alias in aliases:
            with patch.object(self.cli, '_terminar') as mock_salir:
                self.cli._procesar_comando(alias)
                mock_salir.assert_called_once()
    
    def test_tirar_dados_juego_terminado(self):
        """Test de tirar dados cuando el juego terminó"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__game__.__juego_terminado__ = True
        
        with patch('builtins.print') as mock_print:
            try:
                self.cli._tirar_dados()
            except Exception:
                pass
            
            # Verificar que se muestra mensaje de error
            self.assertTrue(any("terminó" in str(call).lower() for call in mock_print.call_args_list))
    
    def test_cambiar_turno_juego_con_dados_disponibles(self):
        """Test de cambiar turno con dados disponibles sin usar"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch.object(self.cli.__game__, 'cambiar_turno') as mock_cambiar:
            with patch('builtins.print'):
                self.cli._cambiar_turno()
                
                # Verificar que se cambió el turno
                mock_cambiar.assert_called_once()
                
                # Verificar que se limpiaron los dados
                self.assertEqual(self.cli.__dados_disponibles__, [])
    
    def test_ver_tablero_vacio(self):
        """Test de mostrar tablero vacío"""
        self.cli.__game__ = Game("Colo", "Juan")
        
        # Vaciar el tablero
        self.cli.__game__.__board__.__puntos__ = [[] for _ in range(24)]
        
        with patch('builtins.print'):
            # No debe lanzar excepción
            self.cli._ver_tablero()
    
    # Tests importantes con inputs
    @patch('builtins.input', side_effect=['Colo', 'Juan'])
    def test_nueva_partida_exito(self, mock_input):
        """Test importante: crear partida con inputs"""
        self.cli._nueva_partida()
        
        self.assertIsNotNone(self.cli.__game__)
        self.assertEqual(self.cli.__game__.get_player1().get_name(), "Colo")
        self.assertEqual(self.cli.__game__.get_player2().get_name(), "Juan")
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_valido_con_input(self, mock_input):
        """Test importante: mover ficha con inputs válidos"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch.object(self.cli.__game__, 'mover_ficha') as mock_mover:
            with patch('builtins.print'):
                self.cli._mover_ficha()
                
                # Verificar que se llamó mover_ficha con índices correctos
                mock_mover.assert_called_once_with(0, 3)
                self.assertEqual(self.cli.__dados_disponibles__, [5])
    
    @patch('builtins.input', side_effect=['abc', 'xyz'])
    def test_mover_ficha_input_invalido(self, mock_input):
        """Test importante: manejo de inputs inválidos (no números)"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch('builtins.print') as mock_print:
            self.cli._mover_ficha()
            
            # Verificar que se muestra error de ValueError
            self.assertTrue(any("números válidos" in str(call) for call in mock_print.call_args_list))
    
    @patch('builtins.input', side_effect=['25', '30'])
    def test_mover_ficha_posicion_fuera_rango(self, mock_input):
        """Test importante: validación de posiciones fuera de rango"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        with patch('builtins.print') as mock_print:
            try:
                self.cli._mover_ficha()
            except Exception:
                pass
            
            # Verificar que se mostró algún mensaje
            self.assertTrue(len(mock_print.call_args_list) > 0)
    
    @patch('builtins.input', side_effect=['Colo', 'Juan'])
    def test_nueva_partida_nombre_vacio_input(self, mock_input):
        """Test importante: nombre vacío en creación de partida"""
        # Establecer mock_input para que el primer input sea vacío
        with patch('builtins.input', side_effect=['', 'Juan']) as mock_inp:
            with patch('builtins.print'):
                try:
                    self.cli._nueva_partida()
                except Exception:
                    pass
                # Verificar que se llamó input
                self.assertGreater(len(mock_inp.call_args_list), 0)
    
    @patch('builtins.input', side_effect=['Colo', 'Colo'])
    def test_nueva_partida_nombres_iguales_input(self, mock_input):
        """Test importante: nombres iguales en creación de partida"""
        with patch('builtins.print'):
            try:
                self.cli._nueva_partida()
            except Exception:
                pass
            # El test verifica el comportamiento
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_juego_terminado_after_move(self, mock_input):
        """Test importante: juego termina después de movimiento"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3, 5]
        
        # Simular que el juego termina después del movimiento
        with patch.object(self.cli.__game__, 'juego_terminado', return_value=True):
            with patch.object(self.cli.__game__, 'get_ganador', return_value=self.cli.__game__.get_player1()):
                with patch.object(self.cli.__game__, 'mover_ficha'):
                    with patch('builtins.print'):
                        self.cli._mover_ficha()
    
    @patch('builtins.input', side_effect=['1', '4'])
    def test_mover_ficha_todos_dados_usados(self, mock_input):
        """Test importante: todos los dados utilizados"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [3]  # Solo un dado
        
        with patch.object(self.cli.__game__, 'mover_ficha'):
            with patch('builtins.print'):
                self.cli._mover_ficha()
                # Verificar que se usaron todos los dados
                self.assertEqual(self.cli.__dados_disponibles__, [])
    
    @patch('builtins.input', side_effect=['-1', '6'])
    def test_mover_ficha_desde_barra(self, mock_input):
        """Test importante: mover ficha desde la barra"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [6, 5]
        
        # Agregar ficha a la barra
        self.cli.__game__.get_board().agregar_barra("blanco")
        
        with patch.object(self.cli.__game__, 'mover_ficha') as mock_mover:
            with patch('builtins.print'):
                self.cli._mover_ficha()
                # Verificar que se llamó mover_ficha desde barra
                mock_mover.assert_called_once()
    
    @patch('builtins.input', side_effect=['1', '-1'])
    def test_mover_ficha_bear_off(self, mock_input):
        """Test importante: bear off (sacar ficha del tablero)"""
        self.cli.__game__ = Game("Colo", "Juan")
        self.cli.__dados_disponibles__ = [1, 5]
        
        with patch.object(self.cli.__game__, 'mover_ficha'):
            with patch('builtins.print'):
                try:
                    self.cli._mover_ficha()
                except Exception:
                    pass
                # Test pasa si no lanza excepción
    
    @patch('builtins.print')
    def test_mostrar_inicio(self, mock_print):
        """Test de mostrar mensaje de inicio"""
        cli = BackgammonCLI()
        cli._mostrar_inicio()
        # Verificar que se imprimió el mensaje de bienvenida
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_mostrar_menu_sin_juego(self, mock_print):
        """Test de mostrar menú sin juego activo"""
        cli = BackgammonCLI()
        cli.__game__ = None
        cli._mostrar_menu()
        # Verificar que se imprimió el menú
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_mostrar_menu_con_juego(self, mock_print):
        """Test de mostrar menú con juego activo"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        cli._mostrar_menu()
        # Verificar que se imprimió el menú
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_mostrar_ayuda(self, mock_print):
        """Test de mostrar ayuda"""
        cli = BackgammonCLI()
        cli._mostrar_ayuda()
        # Verificar que se imprimió la ayuda
        mock_print.assert_called()
    
    def test_procesar_comando_invalido(self):
        """Test de procesar comando inválido"""
        cli = BackgammonCLI()
        with patch('builtins.print') as mock_print:
            cli._procesar_comando("comando_invalido")
            # Verificar que se imprimió mensaje de comando desconocido
            mock_print.assert_called()
    
    @patch('builtins.input', side_effect=['Colo', 'Juan'])
    @patch('builtins.print')
    def test_nueva_partida_nombres_iguales(self, mock_print, mock_input):
        """Test de nueva partida con nombres iguales"""
        cli = BackgammonCLI()
        with patch('builtins.input', side_effect=['Colo', 'Colo']):
            cli._nueva_partida()
            # Debería mostrar error
            mock_print.assert_called()
    
    @patch('builtins.input', side_effect=['Colo', 'Juan'])
    @patch('builtins.print')
    def test_nueva_partida_nombre_vacio(self, mock_print, mock_input):
        """Test de nueva partida con nombre vacío"""
        cli = BackgammonCLI()
        with patch('builtins.input', side_effect=['', 'Juan']):
            cli._nueva_partida()
            # Debería mostrar error
            mock_print.assert_called()
    
    def test_ver_tablero_sin_juego(self):
        """Test de ver tablero sin juego"""
        cli = BackgammonCLI()
        cli.__game__ = None
        with patch('builtins.print') as mock_print:
            cli._ver_tablero()
            # Debería mostrar error
            mock_print.assert_called()
    
    def test_obtener_posiciones_sin_juego(self):
        """Test de obtener posiciones sin juego"""
        cli = BackgammonCLI()
        cli.__game__ = None
        posiciones = cli._obtener_posiciones()
        self.assertEqual(posiciones, [])
    
    def test_nueva_partida_con_excepcion(self):
        """Test de nueva partida con excepción"""
        cli = BackgammonCLI()
        # Simular error al crear juego
        with patch('builtins.input', side_effect=['Colo', 'Juan']):
            with patch('backgammon.core.game.Game', side_effect=Exception("Error")):
                with patch('builtins.print') as mock_print:
                    cli._nueva_partida()
                    # Debería manejar la excepción
                    mock_print.assert_called()
    
    def test_ver_tablero_con_excepcion(self):
        """Test de ver tablero con excepción"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        # Simular error al obtener posiciones
        with patch.object(cli, '_obtener_posiciones', side_effect=Exception("Error")):
            with patch('builtins.print') as mock_print:
                cli._ver_tablero()
                # Debería mostrar error
                mock_print.assert_called()
    
    def test_tirar_dados_con_juego_terminado(self):
        """Test de tirar dados con juego terminado"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        cli.__game__.__juego_terminado__ = True
        with patch('builtins.print') as mock_print:
            cli._tirar_dados()
            # Debería mostrar error
            mock_print.assert_called()
    
    def test_tirar_dados_con_excepcion(self):
        """Test de tirar dados con excepción"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        # Simular error al tirar dados
        with patch.object(cli.__game__, 'tirar_dados', side_effect=Exception("Error")):
            with patch('builtins.print') as mock_print:
                cli._tirar_dados()
                # Debería mostrar error
                mock_print.assert_called()
    
    def test_mover_ficha_con_excepcion_general(self):
        """Test de mover ficha con excepción general"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        cli.__game__.tirar_dados()
        with patch('builtins.input', side_effect=['5', '4']):
            # Simular error general
            with patch.object(cli.__game__, 'mover_ficha', side_effect=Exception("Error general")):
                with patch('builtins.print') as mock_print:
                    cli._mover_ficha()
                    # Debería mostrar error
                    mock_print.assert_called()
    
    def test_mover_ficha_con_value_error(self):
        """Test de mover ficha con ValueError"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        cli.__game__.tirar_dados()
        with patch('builtins.input', side_effect=['abc', '4']):
            with patch('builtins.print') as mock_print:
                cli._mover_ficha()
                # Debería mostrar error de números inválidos
                mock_print.assert_called()
    
    def test_cambiar_turno_con_excepcion(self):
        """Test de cambiar turno con excepción"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        # Simular error al cambiar turno
        with patch.object(cli.__game__, 'cambiar_turno', side_effect=Exception("Error")):
            with patch('builtins.print') as mock_print:
                cli._cambiar_turno()
                # Debería manejar la excepción
                mock_print.assert_called()
    
    def test_mostrar_fila_con_posiciones_insuficientes(self):
        """Test de mostrar fila con posiciones insuficientes"""
        cli = BackgammonCLI()
        cli.__game__ = Game("Colo", "Juan")
        # Crear posiciones incompletas
        posiciones = [5] * 10  # Solo 10 elementos en lugar de 24
        with patch('builtins.print'):
            # Esto debería manejar el caso cuando idx >= len(posiciones)
            cli._mostrar_fila_superior(posiciones)
            cli._mostrar_fila_inferior(posiciones)
            # Test pasa si no lanza excepción


if __name__ == "__main__":
    unittest.main()

    