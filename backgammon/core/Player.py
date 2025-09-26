class Player:
    """
    Clase que representa un jugador en el juego de Backgammon
    """
    
    def __init__(self, nombre, color):
        """
        Inicializa un jugador
        
        Args:
            nombre (str): Nombre del jugador
            color (str): Color de las fichas del jugador ("blanco" o "negro")
            
        Raises:
            ValueError: Si el color no es válido
        """
        if color not in ["blanco", "negro"]:
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        
        self.__nombre__ = nombre
        self.__color__ = color
        self.__fichas_en_juego__ = 15  # Total de fichas en Backgammon
        self.__fichas_en_casa__ = 0    # Fichas que han llegado a casa
        self.__fichas_eliminadas__ = 0 # Fichas que han sido eliminadas
    
    def get_nombre(self):
        """
        Retorna el nombre del jugador
        
        Returns:
            str: Nombre del jugador
        """
        return self.__nombre__
    
    def get_color(self):
        """
        Retorna el color del jugador
        
        Returns:
            str: Color del jugador
        """
        return self.__color__
    
    def get_fichas_en_juego(self):
        """
        Retorna el número de fichas en juego
        
        Returns:
            int: Número de fichas en juego
        """
        return self.__fichas_en_juego__
    
    def get_fichas_en_casa(self):
        """
        Retorna el número de fichas en casa
        
        Returns:
            int: Número de fichas en casa
        """
        return self.__fichas_en_casa__
    
    def get_fichas_eliminadas(self):
        """
        Retorna el número de fichas eliminadas
        
        Returns:
            int: Número de fichas eliminadas
        """
        return self.__fichas_eliminadas__
    
    def mover_ficha_a_casa(self):
        """
        Mueve una ficha a casa (reduce fichas en juego, aumenta fichas en casa)
        """
        if self.__fichas_en_juego__ > 0:
            self.__fichas_en_juego__ -= 1
            self.__fichas_en_casa__ += 1
    
    def eliminar_ficha(self):
        """
        Elimina una ficha del juego
        """
        if self.__fichas_en_juego__ > 0:
            self.__fichas_en_juego__ -= 1
            self.__fichas_eliminadas__ += 1
    
    def reintroducir_ficha(self):
        """
        Reintroduce una ficha eliminada al juego
        """
        if self.__fichas_eliminadas__ > 0:
            self.__fichas_eliminadas__ -= 1
            self.__fichas_en_juego__ += 1
    
    def ha_ganado(self):
        """
        Verifica si el jugador ha ganado (todas las fichas en casa)
        
        Returns:
            bool: True si el jugador ha ganado
        """
        return self.__fichas_en_casa__ == 15
    
    def __str__(self):
        """
        Representación en string del jugador
        
        Returns:
            str: Representación del jugador
        """
        return f"{self.__nombre__} ({self.__color__})"
    
    def __eq__(self, other):
        """
        Compara dos jugadores por nombre y color
        
        Args:
            other: Otro jugador
            
        Returns:
            bool: True si son iguales
        """
        if not isinstance(other, Player):
            return False
        return (self.__nombre__ == other.__nombre__ and 
                self.__color__ == other.__color__)
