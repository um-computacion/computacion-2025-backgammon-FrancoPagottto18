from backgammon.core.board import Board
from backgammon.core.Player import Player
from backgammon.core.dice import Dice
from backgammon.core.exceptions import GameError, MovimientoInvalidoError, JuegoTerminadoError


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
    
    def get_board(self):
        """
        Retorna el tablero del juego
        
        Returns:
            Board: El tablero actual
        """
        return self.__board__
    
    def get_player1(self):
        """
        Retorna el primer jugador
        
        Returns:
            Player: Jugador 1 (blanco)
        """
        return self.__player1__
    
    def get_player2(self):
        """
        Retorna el segundo jugador
        
        Returns:
            Player: Jugador 2 (negro)
        """
        return self.__player2__
    
    def get_dice(self):
        """
        Retorna los dados del juego
        
        Returns:
            Dice: Los dados del juego
        """
        return self.__dice__
    
    def get_turno_actual(self):
        """
        Retorna el jugador que tiene el turno actual
        
        Returns:
            Player: Jugador actual
        """
        return self.__turno_actual__
    
    def cambiar_turno(self):
        """
        Cambia el turno al siguiente jugador
        """
        if self.__turno_actual__ == self.__player1__:
            self.__turno_actual__ = self.__player2__
        else:
            self.__turno_actual__ = self.__player1__
    
    def tirar_dados(self):
        """
        Tira los dados y retorna los valores
        
        Returns:
            list: Lista con los valores de los dados
            
        Raises:
            JuegoTerminadoError: Si el juego ya terminó
        """
        if self.__juego_terminado__:
            raise JuegoTerminadoError("No se pueden tirar dados en un juego terminado")
        
        return self.__dice__.tirar()
    
    def mover_ficha(self, desde, hacia):
        """
        Mueve una ficha en el tablero
        
        Args:
            desde (int): Punto de origen (-1 para fichas eliminadas)
            hacia (int): Punto de destino (-1 para eliminar ficha)
            
        Raises:
            JuegoTerminadoError: Si el juego ya terminó
            MovimientoInvalidoError: Si el movimiento no es válido
        """
        if self.__juego_terminado__:
            raise JuegoTerminadoError("No se pueden hacer movimientos en un juego terminado")
        
        color_actual = self.__turno_actual__.get_color()
        self.__board__.mover_ficha(desde, hacia, color_actual)
        
        # Si se movió una ficha a casa, actualizar el jugador
        if hacia == -1:  # Ficha eliminada
            self.__turno_actual__.eliminar_ficha()
        elif self.__es_casa_jugador__(hacia, color_actual):
            self.__turno_actual__.mover_ficha_a_casa()
    
  