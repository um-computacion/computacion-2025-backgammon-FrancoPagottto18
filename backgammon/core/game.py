from backgammon.core.board import Board
from backgammon.core.Player import Player
from backgammon.core.dice import Dice
from backgammon.core.exceptions import GameError, MovimientoInvalidoError, JuegoTerminadoError


class Game:
    """
    Clase principal que coordina el flujo general del juego de Backgammon
    """
    def __init__(self, nombre_jugador1, nombre_jugador2):
        """
        Inicializa una nueva partida de Backgammon
        
        Args:
            nombre_jugador1 (str): Nombre del primer jugador
            nombre_jugador2 (str): Nombre del segundo jugador
            
        Raises:
            ValueError: Si los nombres son inválidos
        """
        if not nombre_jugador1 or not nombre_jugador2:
            raise ValueError("Los nombres de los jugadores no pueden estar vacíos")
        if nombre_jugador1 == nombre_jugador2:
            raise ValueError("Los nombres de los jugadores deben ser diferentes")
        
        self.__board__ = Board()
        self.__player1__ = Player(nombre_jugador1, "blanco")
        self.__player2__ = Player(nombre_jugador2, "negro")
        self.__dice__ = Dice()
        self.__turno_actual__ = self.__player1__  
        self.__juego_terminado__ = False
        self.__ganador__ = None
    
    def get_board(self):
        """
        Retorna el tablero del juego
        
        Returns:
            Board: El tablero actual
        """
        return self.__board__
    
    def get_player1(self):
        """
        Retorna el primer jugador
        
        Returns:
            Player: Jugador 1 (blanco)
        """
        return self.__player1__
    
    def get_player2(self):
        """
        Retorna el segundo jugador
        
        Returns:
            Player: Jugador 2 (negro)
        """
        return self.__player2__
    
    def get_dice(self):
        """
        Retorna los dados del juego
        
        Returns:
            Dice: Los dados del juego
        """
        return self.__dice__
    
    def get_turno_actual(self):
        """
        Retorna el jugador que tiene el turno actual
        
        Returns:
            Player: Jugador actual
        """
        return self.__turno_actual__
    
    def cambiar_turno(self):
        """
        Cambia el turno al siguiente jugador
        """
        if self.__turno_actual__ == self.__player1__:
            self.__turno_actual__ = self.__player2__
        else:
            self.__turno_actual__ = self.__player1__
    
    def tirar_dados(self):
        """
        Tira los dados y retorna los valores
        
        Returns:
            list: Lista con los valores de los dados
            
        Raises:
            JuegoTerminadoError: Si el juego ya terminó
        """
        if self.__juego_terminado__:
            raise JuegoTerminadoError("No se pueden tirar dados en un juego terminado")
        
        return self.__dice__.tirar()
    
    def mover_ficha(self, desde, hacia):
        """
        Mueve una ficha en el tablero
        
        Args:
            desde (int): Punto de origen (-1 para fichas en barra)
            hacia (int): Punto de destino (-1 para eliminar ficha)
            
        Raises:
            JuegoTerminadoError: Si el juego ya terminó
            MovimientoInvalidoError: Si el movimiento no es válido
        """
        if self.__juego_terminado__:
            raise JuegoTerminadoError("No se pueden hacer movimientos en un juego terminado")
        
        color_actual = self.__turno_actual__.get_color()
        
        # Validar posiciones
        if desde != -1 and not 0 <= desde <= 23:
            raise ValueError("La posición de origen debe estar entre 0 y 23 o ser -1")
        if hacia != -1 and not 0 <= hacia <= 23:
            raise ValueError("La posición de destino debe estar entre 0 y 23 o ser -1")
        
        # No se puede mover al mismo punto
        if desde == hacia:
            raise MovimientoInvalidoError("No se puede mover una ficha al mismo punto")
        
        # Verificar que hay fichas en el punto de origen
        if desde == -1:
            # Mover desde la barra
            if len(self.__board__.get_barra()[color_actual]) == 0:
                raise MovimientoInvalidoError("No hay fichas en la barra para reintroducir")
        else:
            # Mover desde un punto del tablero
            puntos = self.__board__.get_puntos()
            if len(puntos[desde]) == 0:
                raise MovimientoInvalidoError(f"No hay fichas en el punto {desde}")
            if puntos[desde][0].get_color() != color_actual:
                raise MovimientoInvalidoError(f"Las fichas en el punto {desde} no son del color {color_actual}")
        
        # Verificar destino
        if hacia == -1:
            # Eliminar ficha (llevar a casa)
            if desde == -1:
                raise MovimientoInvalidoError("No se puede eliminar una ficha ya en la barra")
        else:
            # Mover a un punto del tablero
            puntos = self.__board__.get_puntos()
            
            # Verificar si el punto está ocupado por el oponente
            if len(puntos[hacia]) > 0 and puntos[hacia][0].get_color() != color_actual:
                if len(puntos[hacia]) > 1:
                    raise MovimientoInvalidoError(f"El punto {hacia} está bloqueado por el oponente")
                # Si hay solo una ficha del oponente, se puede "comer"
                ficha_comida = puntos[hacia][0]
                self.__board__.quitar_ficha(hacia)
                self.__board__.agregar_barra(ficha_comida.get_color())
          
        # Realizar el movimiento
        if desde == -1:
            # Reintroducir ficha desde la barra
            self.__board__.quitar_barra(color_actual)
        else:
            # Mover desde un punto del tablero
            self.__board__.quitar_ficha(desde)
        
        if hacia != -1:
            # Mover a un punto del tablero
            self.__board__.agregar_ficha(color_actual, hacia)
         
    def verificar_ganador(self):
        """
        Verifica si hay un ganador y actualiza el estado del juego
        
        Returns:
            Player or None: El ganador si existe, None si no hay ganador aún
        """
        # Verificar si algún jugador tiene todas sus fichas en casa
        puntos = self.__board__.get_puntos()
        
        # Verificar jugador blanco (casa: puntos 18-23)
        fichas_blancas_en_casa = 0
        for i in range(18, 24):
            for ficha in puntos[i]:
                if ficha.get_color() == "blanco":
                    fichas_blancas_en_casa += 1
        
        # Verificar jugador negro (casa: puntos 0-5)
        fichas_negras_en_casa = 0
        for i in range(6):
            for ficha in puntos[i]:
                if ficha.get_color() == "negro":
                    fichas_negras_en_casa += 1
        
        if fichas_blancas_en_casa == 15:
            self.__juego_terminado__ = True
            self.__ganador__ = self.__player1__
            return self.__player1__
        elif fichas_negras_en_casa == 15:
            self.__juego_terminado__ = True
            self.__ganador__ = self.__player2__
            return self.__player2__
        return None
    
    def get_ganador(self):
        """
        Retorna el ganador del juego
        
        Returns:
            Player or None: El ganador si existe, None si no hay ganador
        """
        return self.__ganador__
    
    def juego_terminado(self):
        """
        Verifica si el juego ha terminado
        
        Returns:
            bool: True si el juego ha terminado
        """
        return self.__juego_terminado__
    
    def reiniciar_juego(self):
        """
        Reinicia el juego a su estado inicial
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__turno_actual__ = self.__player1__
        self.__juego_terminado__ = False
        self.__ganador__ = None
   
    
        
       