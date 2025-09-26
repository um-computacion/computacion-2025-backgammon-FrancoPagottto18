from backgammon.core.exceptions import MovimientoInvalidoError


class Board:
    """
    Clase que maneja el tablero de Backgammon
    """
    
    def __init__(self):
        """
        Inicializa el tablero con la configuración inicial de Backgammon
        """
        # El tablero tiene 24 puntos numerados del 0 al 23
        # Cada punto puede tener fichas de un color
        # Posición inicial según las reglas de Backgammon:
        # Punto 0: 2 fichas blancas (casa del jugador blanco)
        # Punto 5: 5 fichas negras
        # Punto 7: 3 fichas negras
        # Punto 11: 5 fichas blancas
        # Punto 12: 5 fichas negras
        # Punto 16: 3 fichas blancas
        # Punto 18: 5 fichas blancas
        # Punto 23: 2 fichas negras (casa del jugador negro)
        
        self.__puntos__ = [0] * 24  # Cada punto contiene el número de fichas
        self.__colores__ = [None] * 24  # Color de las fichas en cada punto
        
        # Configuración inicial
        self.__puntos__[0] = 2
        self.__colores__[0] = "blanco"
        
        self.__puntos__[5] = 5
        self.__colores__[5] = "negro"
        
        self.__puntos__[7] = 3
        self.__colores__[7] = "negro"
        
        self.__puntos__[11] = 5
        self.__colores__[11] = "blanco"
        
        self.__puntos__[12] = 5
        self.__colores__[12] = "negro"
        
        self.__puntos__[16] = 3
        self.__colores__[16] = "blanco"
        
        self.__puntos__[18] = 5
        self.__colores__[18] = "blanco"
        
        self.__puntos__[23] = 2
        self.__colores__[23] = "negro"
        
        # Fichas eliminadas (bar)
        self.__fichas_eliminadas_blancas__ = 0
        self.__fichas_eliminadas_negras__ = 0
    
    def get_punto(self, posicion):
        """
        Retorna información sobre un punto específico
        
        Args:
            posicion (int): Posición del punto (0-23)
            
        Returns:
            tuple: (numero_fichas, color) o (0, None) si está vacío
            
        Raises:
            ValueError: Si la posición no es válida
        """
        if not 0 <= posicion <= 23:
            raise ValueError("La posición debe estar entre 0 y 23")
        
        return (self.__puntos__[posicion], self.__colores__[posicion])
    
    def get_tablero_completo(self):
        """
        Retorna el estado completo del tablero
        
        Returns:
            list: Lista de tuplas (numero_fichas, color) para cada punto
        """
        return [(self.__puntos__[i], self.__colores__[i]) for i in range(24)]
    
    def get_fichas_eliminadas(self, color):
        """
        Retorna el número de fichas eliminadas de un color
        
        Args:
            color (str): Color de las fichas ("blanco" o "negro")
            
        Returns:
            int: Número de fichas eliminadas
            
        Raises:
            ValueError: Si el color no es válido
        """
        if color not in ["blanco", "negro"]:
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        
        if color == "blanco":
            return self.__fichas_eliminadas_blancas__
        else:
            return self.__fichas_eliminadas_negras__
    
    def mover_ficha(self, desde, hacia, color):
        """
        Mueve una ficha de un punto a otro
        
        Args:
            desde (int): Punto de origen (0-23, o -1 para fichas eliminadas)
            hacia (int): Punto de destino (0-23, o -1 para eliminar)
            color (str): Color de las fichas
            
        Raises:
            MovimientoInvalidoError: Si el movimiento no es válido
            ValueError: Si los parámetros no son válidos
        """
        if color not in ["blanco", "negro"]:
            raise ValueError("El color debe ser 'blanco' o 'negro'")
        
        # Validar posiciones
        if desde != -1 and not 0 <= desde <= 23:
            raise ValueError("La posición de origen debe estar entre 0 y 23 o ser -1")
        if hacia != -1 and not 0 <= hacia <= 23:
            raise ValueError("La posición de destino debe estar entre 0 y 23 o ser -1")
        
        # Verificar que hay fichas en el punto de origen
        if desde == -1:
            # Mover desde fichas eliminadas
            fichas_eliminadas = self.get_fichas_eliminadas(color)
            if fichas_eliminadas == 0:
                raise MovimientoInvalidoError("No hay fichas eliminadas para reintroducir")
        else:
            # Mover desde un punto del tablero
            fichas_origen, color_origen = self.get_punto(desde)
            if fichas_origen == 0:
                raise MovimientoInvalidoError(f"No hay fichas en el punto {desde}")
            if color_origen != color:
                raise MovimientoInvalidoError(f"Las fichas en el punto {desde} no son del color {color}")
        
        # Verificar destino
        if hacia == -1:
            # Eliminar ficha
            if desde == -1:
                raise MovimientoInvalidoError("No se puede eliminar una ficha ya eliminada")
        else:
            # Mover a un punto del tablero
            fichas_destino, color_destino = self.get_punto(hacia)
            
            # Verificar si el punto está ocupado por el oponente
            if fichas_destino > 0 and color_destino != color:
                if fichas_destino > 1:
                    raise MovimientoInvalidoError(f"El punto {hacia} está bloqueado por el oponente")
                # Si hay solo una ficha del oponente, se puede "comer"
                self.__puntos__[hacia] = 0
                self.__colores__[hacia] = None
                # La ficha del oponente va a la barra
                if color == "blanco":
                    self.__fichas_eliminadas_negras__ += 1
                else:
                    self.__fichas_eliminadas_blancas__ += 1
        
        # Realizar el movimiento
        if desde == -1:
            # Reintroducir ficha eliminada
            if color == "blanco":
                self.__fichas_eliminadas_blancas__ -= 1
            else:
                self.__fichas_eliminadas_negras__ -= 1
        else:
            # Mover desde un punto del tablero
            self.__puntos__[desde] -= 1
            if self.__puntos__[desde] == 0:
                self.__colores__[desde] = None
        
        if hacia != -1:
            # Mover a un punto del tablero
            self.__puntos__[hacia] += 1
            self.__colores__[hacia] = color
    
    def es_movimiento_valido(self, desde, hacia, color):
        """
        Verifica si un movimiento es válido sin ejecutarlo
        
        Args:
            desde (int): Punto de origen
            hacia (int): Punto de destino
            color (str): Color de las fichas
            
        Returns:
            bool: True si el movimiento es válido
        """
        try:
            # Crear una copia temporal del tablero para probar el movimiento
            tablero_original = (self.__puntos__[:], self.__colores__[:], 
                              self.__fichas_eliminadas_blancas__, 
                              self.__fichas_eliminadas_negras__)
            
            self.mover_ficha(desde, hacia, color)
            
            # Restaurar el tablero original
            (self.__puntos__, self.__colores__, 
             self.__fichas_eliminadas_blancas__, 
             self.__fichas_eliminadas_negras__) = tablero_original
            
            return True
        except (MovimientoInvalidoError, ValueError):
            return False
    
    def get_puntos_con_fichas(self, color):
        """
        Retorna los puntos que tienen fichas del color especificado
        
        Args:
            color (str): Color de las fichas
            
        Returns:
            list: Lista de posiciones que tienen fichas del color
        """
        puntos = []
        for i in range(24):
            if self.__colores__[i] == color and self.__puntos__[i] > 0:
                puntos.append(i)
        return puntos
    
    def puede_reintroducir(self, color):
        """
        Verifica si un jugador puede reintroducir fichas eliminadas
        
        Args:
            color (str): Color del jugador
            
        Returns:
            bool: True si puede reintroducir fichas
        """
        return self.get_fichas_eliminadas(color) > 0
    
    def __str__(self):
        """
        Representación en string del tablero
        
        Returns:
            str: Representación visual del tablero
        """
        resultado = "Tablero de Backgammon:\n"
        resultado += "Puntos: "
        for i in range(24):
            if self.__puntos__[i] > 0:
                color_char = "B" if self.__colores__[i] == "blanco" else "N"
                resultado += f"{i}:{self.__puntos__[i]}{color_char} "
        resultado += f"\nFichas eliminadas - Blancas: {self.__fichas_eliminadas_blancas__}, Negras: {self.__fichas_eliminadas_negras__}"
        return resultado
