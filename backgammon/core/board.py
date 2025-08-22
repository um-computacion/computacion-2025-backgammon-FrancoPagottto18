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