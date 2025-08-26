
from .checker import Checker
class Board:
    """
    Representa el tablero de la partida de backgammon
    
    Atributos:
    __puntos__ (list):lista de 24 listas,cada una representa un punto en el tablero
    __barra__(dict):Fichas capturadas de cada jugador
    """
    def __init__(self):
        """
        Inicializa el tablero con la configuración estandar del Backgammon
        """
        self.__puntos__=[[]for _ in range(24)]
        self.__barra__={"X":[],"O" : []}
        self.inicializar_tablero()
    def inicializar_tablero(self):
        """
        Coloca las fichas en la posición inicial estándar de Backgammon usando objetos Checker
        """
        self.__puntos__ = [[] for _ in range(24)]
        # Fichas del jugador X
        self.__puntos__[23] = [Checker("negro"), Checker("negro")]                
        self.__puntos__[12] = [Checker("negro") for _ in range(5)]             
        self.__puntos__[7]  = [Checker("negro") for _ in range(3)]             
        self.__puntos__[5]  = [Checker("negro") for _ in range(5)]             
        # Fichas del jugador O
        self.__puntos__[0]  = [Checker("blanco"), Checker("blanco")]                
        self.__puntos__[11] = [Checker("blanco") for _ in range(5)]             
        self.__puntos__[16] = [Checker("blanco") for _ in range(3)]             
        self.__puntos__[18] = [Checker("blanco") for _ in range(5)]             
        # Limpio la barra
        self.__barra__ = {"X": [], "O": []}

