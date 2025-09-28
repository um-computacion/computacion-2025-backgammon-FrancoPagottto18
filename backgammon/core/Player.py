class Player:
    def __init__(self, nombre, color):
        self.__nombre__ = nombre
        self.__color__ = color

    def get_name(self):
        return self.__nombre__
    
    def get_color(self):
        return self.__color__