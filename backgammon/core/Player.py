class Player:
    """
    Representa a un jugador en el juego 
    Atributos:
    __nombre__ (str): El nombre del jugador
    __simbolo__ (str): El color de las fichas del jugador
    """
    def __init__(self, nombre, simbolo):
        self.__nombre__ = nombre
        self.__simbolo__ = simbolo