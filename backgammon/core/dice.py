import random

class Dice:
    def __init__(self):
        """
        Inicializa dos dados de seis caras
        """
        self.__dado1__ = 0
        self.__dado2__ = 0
        self.__tirada_doble__ = False
    def tirar(self):
        """
        Tira los dos dados y retorna los valores
        Si es doble, los valores se repiten
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        self.__tirada_doble__ = (self.__dado1__ == self.__dado2__)
        return self.get_valores()