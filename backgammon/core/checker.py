class Checker:
    """
    Representa una ficha de Backgammon
    Atributos:
        __color__ (str): Color o símbolo del jugador al que pertenece la ficha ("X" o "O")
    """
    def __init__(self, color):
        """
        Inicializa una ficha con el color/símbolo del jugador
        Args:
            color (str): "X" o "O" según el jugador
        """
        self.__color__ = color

    def get_color(self):
        """Devuelve el color/símbolo de la ficha."""
        return self.__color__

    def __str__(self):
        return self.__color__
