#!/usr/bin/env python3

"""
Interfaz de línea de comandos para el juego de Backgammon
"""

import sys
from backgammon.core.game import Game
from backgammon.core.exceptions import MovimientoInvalidoError, JuegoTerminadoError


class BackgammonCLI:
    """
    Interfaz de línea de comandos para el juego de Backgammon
    """
    
    def __init__(self):
        """
        Inicializa la CLI
        """
        self.__game__ = None

    def run(self):
        """
        Ejecuta el bucle principal de la CLI
        """
        self._display_welcome()
        
        while True:
            try:
                if self.__game__ and not self.__game__.juego_terminado():
                    self._display_game_menu()
                else:
                    self._display_main_menu()

                command = input("Ingrese comando: ").strip().lower()
                
                if command in ["nueva", "n", "1"]:
                    self._start_new_game()
                elif command in ["tablero", "t"]:
                    self._display_board()
                elif command in ["tirar", "dados", "d"]:
                    self._roll_dice()
                elif command in ["mover", "m"]:
                    self._move_checker()
                elif command in ["ayuda", "help", "h"]:
                    self._display_help()
                elif command in ["salir", "s", "exit"]:
                    self._exit_game()
                else:
                    print("Comando no reconocido. Ingrese 'ayuda' para ver comandos.")
                    
            except KeyboardInterrupt:
                print("\n¡Hasta luego!")
                break
            except EOFError:
                print("\n¡Hasta luego!")
                break

    def _display_welcome(self):
        """
        Muestra el mensaje de bienvenida
        """
        print("=" * 50)
        print("BACKGAMMON - JUEGO DE MESA".center(50))
        print("=" * 50)
        print("Objetivo: Llevar 15 fichas a casa".center(50))
        print("=" * 50)

    def _display_main_menu(self):
        """
        Muestra el menú principal
        """
        print("\nMENÚ PRINCIPAL:")
        print("1. nueva - Iniciar partida")
        print("2. ayuda - Ver ayuda")
        print("3. salir - Salir")

    def _display_game_menu(self):
        """
        Muestra el menú del juego activo
        """
        jugador = self.__game__.get_turno_actual()
        print(f"\nTurno: {jugador.get_name()} ({jugador.get_color()})")
        print("Comandos: tablero, tirar, mover, nueva, salir")

 