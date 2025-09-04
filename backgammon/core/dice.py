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
     def get_valores(self):
        """
        Retorna lista con los valores de los dados,si es doble, repite el valor 4 veces
        """
        if self.__tirada_doble__:
            return [self.__dado1__] * 4  
        else:
            return [self.__dado1__, self.__dado2__]

    def es_doble(self):
        """
        Retorna True si la última tirada fue doble
        """
        return self.__tirada_doble__