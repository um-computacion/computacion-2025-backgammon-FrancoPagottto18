from backgammon.core.Player import Player
from backgammon.core.checker import Checker
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
        self.__barra__={"blanco":[],"negro":[]}
        self.inicializar_tablero()
    def inicializar_tablero(self):
        """
        Coloca las fichas en la posición inicial estándar de Backgammon usando objetos Checker
        """
        self.__puntos__ = [[] for _ in range(24)]
        # Fichas del jugador blanco
        self.__puntos__[23] = [Checker("blanco"), Checker("blanco")]                
        self.__puntos__[12] = [Checker("blanco") for _ in range(5)]             
        self.__puntos__[7]  = [Checker("blanco") for _ in range(3)]             
        self.__puntos__[5]  = [Checker("blanco") for _ in range(5)]             
        # Fichas del jugador O
        self.__puntos__[0]  = [Checker("negro"), Checker("negro")]                
        self.__puntos__[11] = [Checker("negro") for _ in range(5)]             
        self.__puntos__[16] = [Checker("negro") for _ in range(3)]             
        self.__puntos__[18] = [Checker("negro") for _ in range(5)]             
        # Limpio la barra
        self.__barra__ = {"blanco": [], "negro": []}
    def agregar_ficha(self, color, punto):
        """
        Agrega una ficha a un punto del tablero
        """
        self.__puntos__[punto].append(Checker(color))
    def quitar_ficha(self, punto):
        """
        Quita una ficha de un punto del tablero
        """
        if self.__puntos__[punto] == []:
            return False
        else:
            self.__puntos__[punto].pop()                

            return True
    
    def agregar_barra(self, color):
        """
        Agrega una ficha a la barra
        """
        self.__barra__[color].append(Checker(color))
    def quitar_barra(self, color):
        """
        Quita una ficha de la barra
        """
        if self.__barra__[color] == []:
            return False
        else:
            self.__barra__[color].remove(Checker(color))
            return True
  