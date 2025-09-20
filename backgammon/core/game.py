from backgammon.core.board import Board
from backgammon.core.Player import Player
from backgammon.core.dice import Dice
from backgammon.core.exceptions import GameError, MovimientoInvalidoError


class Game:
    """
    Clase principal que maneja la lógica del juego de Backgammon
    """
    def __init__(self, nombre_jugador1, nombre_jugador2):
        """
        Inicializa una nueva partida de Backgammon
        Args:
            nombre_jugador1 (str): Nombre del primer jugador
            nombre_jugador2 (str): Nombre del segundo jugador
        Raises:
            ValueError: Si los nombres son inválidos
        """
        if not nombre_jugador1 or not nombre_jugador2:
            raise ValueError("Los nombres de los jugadores no pueden estar vacíos")
        if nombre_jugador1 == nombre_jugador2:
            raise ValueError("Los nombres de los jugadores deben ser diferentes")
        self.__board__ = Board()
        self.__player1__ = Player(nombre_jugador1, "blanco")
        self.__player2__ = Player(nombre_jugador2, "negro")
        self.__dice__ = Dice()
        self.__turno_actual__ = self.__player1__  
        self.__juego_terminado__ = False
        self.__ganador__ = None
  