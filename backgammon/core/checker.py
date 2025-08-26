class Checker:
    """
    Representa una ficha de Backgammon
    """
    def __init__(self, color):
        """
        Inicializa una ficha con el color del jugador
        """
        self.__color__ = color

    def get_color(self):
        """Devuelve el color de la ficha"""
        return self.__color__

    def __str__(self):
        return self.__color__