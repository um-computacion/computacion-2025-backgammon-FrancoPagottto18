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
        self.__tipo_victoria__ = None  # "simple", "gammon", "backgammon"
        self.__fichas_sacadas__ = {"blanco": 0, "negro": 0}  # Contador de fichas sacadas por bear off
    
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
    
    def mover_ficha(self, desde, hacia, valor_dado=None):
        """
        Mueve una ficha en el tablero
        
        Args:
            desde (int): Punto de origen (-1 para fichas en barra)
            hacia (int): Punto de destino (-1 para eliminar ficha)
            valor_dado (int): Valor del dado a usar para el movimiento
            
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
        
        # Validar distancia del movimiento (reglas del Backgammon)
        if valor_dado is not None:
            distancia = self._calcular_distancia(desde, hacia, color_actual)
            # Para bear off (hacia == -1), permitir dados mayores o iguales
            if hacia == -1:
                if valor_dado < distancia:
                    raise MovimientoInvalidoError(f"El dado ({valor_dado}) es menor que la distancia necesaria ({distancia}) para guardar esta ficha")
            else:
                # Para movimientos normales, debe ser exacto
                if distancia != valor_dado:
                    raise MovimientoInvalidoError(f"El movimiento debe usar exactamente el valor del dado ({valor_dado}), distancia: {distancia}")
        
        # Verificar destino
        if hacia == -1:
            # Eliminar ficha (llevar a casa - bear off)
            if desde == -1:
                raise MovimientoInvalidoError("No se puede eliminar una ficha ya en la barra")
            # Verificar que el jugador pueda hacer bear off
            if not self._puede_hacer_bear_off(color_actual):
                cuadrante_casa = "puntos 1-6" if color_actual == "blanco" else "puntos 19-24"
                raise MovimientoInvalidoError(f"Solo puedes sacar fichas cuando todas tus fichas están en tu cuadrante de casa ({cuadrante_casa})")
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
        else:
            # Bear off: la ficha se saca del tablero
            self.__fichas_sacadas__[color_actual] += 1
        
        # Verificar si el movimiento resultó en una victoria
        self.verificar_ganador()
    
    def _calcular_distancia(self, desde, hacia, color):
        """
        Calcula la distancia entre dos puntos considerando la dirección del jugador
        
        Args:
            desde (int): Punto de origen
            hacia (int): Punto de destino (-1 para bear off)
            color (str): Color del jugador
            
        Returns:
            int: Distancia entre los puntos
        """
        if desde == -1:  # Desde la barra
            if hacia == -1:  # Bear off desde barra (no permitido)
                raise MovimientoInvalidoError("No se puede sacar una ficha desde la barra")
            if color == "blanco":
                # Jugador blanco reintroduce en el cuadrante del oponente (puntos 19-24, índices 18-23)
                # Dado 1 → punto 24 (idx 23), dado 6 → punto 19 (idx 18)
                if hacia < 18:  # Solo puede entrar en puntos 19-24
                    raise MovimientoInvalidoError("Blanco solo puede reintroducir en puntos 19-24")
                return 24 - hacia  # Dado 1 = distancia 1 (hacia idx=23), dado 6 = distancia 6 (hacia idx=18)
            else:
                # Jugador negro reintroduce en el cuadrante del oponente (puntos 1-6, índices 0-5)
                # Dado 1 → punto 1 (idx 0), dado 6 → punto 6 (idx 5)
                if hacia > 5:  # Solo puede entrar en puntos 1-6
                    raise MovimientoInvalidoError("Negro solo puede reintroducir en puntos 1-6")
                return hacia + 1  # Dado 1 = distancia 1 (hacia idx=0), dado 6 = distancia 6 (hacia idx=5)
        
        if hacia == -1:  # Bear off (sacando ficha)
            if color == "blanco":
                # Blanco: distancia desde punto actual hasta casa (punto 0)
                return desde + 1
            else:
                # Negro: distancia desde punto actual hasta casa (punto 23)
                return 24 - desde
        
        # Para el Backgammon, los jugadores deben avanzar siempre en su dirección:
        # - Blanco: de 24 a 1 (índices 23 a 0), es decir, índices decrecientes
        # - Negro: de 1 a 24 (índices 0 a 23), es decir, índices crecientes
        if color == "blanco":
            # Blanco retrocede si hacia > desde
            if hacia > desde:
                raise MovimientoInvalidoError("El jugador blanco no puede retroceder")
            return desde - hacia
        else:
            # Negro retrocede si hacia < desde
            if hacia < desde:
                raise MovimientoInvalidoError("El jugador negro no puede retroceder")
            return hacia - desde
    
    def _puede_hacer_bear_off(self, color):
        """
        Verifica si el jugador puede hacer bear off (sacar fichas del tablero)
        Un jugador solo puede hacer bear off si TODAS sus fichas están en su cuadrante de casa
        
        Args:
            color (str): Color del jugador ("blanco" o "negro")
            
        Returns:
            bool: True si puede hacer bear off, False en caso contrario
        """
        puntos = self.__board__.get_puntos()
        barra = self.__board__.get_barra()
        
        # Verificar que no haya fichas en la barra (deben ser reintroducidas primero)
        if len(barra[color]) > 0:
            return False
        
        # Verificar que todas las fichas estén en el cuadrante de casa
        # BLANCO: puntos 0-17 (índices 0-17, pero cuadrante de casa es 0-5)
        # NEGRO: puntos 7-24 (índices 6-23, pero cuadrante de casa es 18-23)
        
        if color == "blanco":
            # Blanco: cuadrante de casa son los puntos 1-6 (índices 0-5)
            cuadrante_casa = list(range(6))
        else:
            # Negro: cuadrante de casa son los puntos 19-24 (índices 18-23)
            cuadrante_casa = list(range(18, 24))
        
        # Verificar que todas las fichas del jugador estén en su cuadrante de casa
        for i, punto in enumerate(puntos):
            for ficha in punto:
                if ficha.get_color() == color:
                    if i not in cuadrante_casa:
                        return False
        
        return True
         
    def verificar_ganador(self):
        """
        Verifica si hay un ganador y actualiza el estado del juego
        Un jugador gana cuando no tiene más fichas en el tablero ni en la barra
        
        Returns:
            Player or None: El ganador si existe, None si no hay ganador aún
        """
        puntos = self.__board__.get_puntos()
        barra = self.__board__.get_barra()
        
        # Contar fichas del jugador blanco en el tablero y en la barra
        fichas_blancas_en_tablero = 0
        for punto in puntos:
            for ficha in punto:
                if ficha.get_color() == "blanco":
                    fichas_blancas_en_tablero += 1
        
        fichas_blancas_en_barra = len(barra["blanco"])
        total_fichas_blancas = fichas_blancas_en_tablero + fichas_blancas_en_barra
        
        # Contar fichas del jugador negro en el tablero y en la barra
        fichas_negras_en_tablero = 0
        for punto in puntos:
            for ficha in punto:
                if ficha.get_color() == "negro":
                    fichas_negras_en_tablero += 1
        
        fichas_negras_en_barra = len(barra["negro"])
        total_fichas_negras = fichas_negras_en_tablero + fichas_negras_en_barra
        
        # Si un jugador no tiene fichas en el tablero ni en la barra, gana
        # El ganador es el jugador que acaba de hacer el movimiento (__turno_actual__)
        if total_fichas_blancas == 0:
            self.__juego_terminado__ = True
            self.__ganador__ = self.__turno_actual__
            # Determinar tipo de victoria basado en el estado del oponente
            if total_fichas_negras == 0:
                # Ambos llegaron a 0 (no debería pasar en partida normal)
                self.__tipo_victoria__ = "simple"
            elif self.__fichas_sacadas__["negro"] == 0:
                # Negro no ha sacado ninguna ficha: verificar si está en casa blanca o barra
                if fichas_negras_en_barra > 0:
                    # Negro tiene fichas en la barra: BACKGAMMON (triple)
                    self.__tipo_victoria__ = "backgammon"
                elif fichas_negras_en_tablero > 0:
                    # Verificar si negro tiene fichas en la casa de blanco (puntos 0-5)
                    fichas_negras_en_casa_blanca = 0
                    for i in range(6):
                        for ficha in puntos[i]:
                            if ficha.get_color() == "negro":
                                fichas_negras_en_casa_blanca += 1
                    if fichas_negras_en_casa_blanca > 0:
                        self.__tipo_victoria__ = "backgammon"
                    else:
                        self.__tipo_victoria__ = "gammon"
                else:
                    self.__tipo_victoria__ = "gammon"
            else:
                # Negro ha sacado al menos 1 ficha: victoria simple
                self.__tipo_victoria__ = "simple"
            return self.__turno_actual__
        elif total_fichas_negras == 0:
            self.__juego_terminado__ = True
            self.__ganador__ = self.__turno_actual__
            # Determinar tipo de victoria basado en el estado del oponente
            if self.__fichas_sacadas__["blanco"] == 0:
                # Blanco no ha sacado ninguna ficha: verificar si está en casa negra o barra
                if fichas_blancas_en_barra > 0:
                    # Blanco tiene fichas en la barra: BACKGAMMON (triple)
                    self.__tipo_victoria__ = "backgammon"
                elif fichas_blancas_en_tablero > 0:
                    # Verificar si blanco tiene fichas en la casa de negro (puntos 18-23)
                    fichas_blancas_en_casa_negra = 0
                    for i in range(18, 24):
                        for ficha in puntos[i]:
                            if ficha.get_color() == "blanco":
                                fichas_blancas_en_casa_negra += 1
                    if fichas_blancas_en_casa_negra > 0:
                        self.__tipo_victoria__ = "backgammon"
                    else:
                        self.__tipo_victoria__ = "gammon"
                else:
                    self.__tipo_victoria__ = "gammon"
            else:
                # Blanco ha sacado al menos 1 ficha: victoria simple
                self.__tipo_victoria__ = "simple"
            return self.__turno_actual__
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
    
    def get_tipo_victoria(self):
        """
        Retorna el tipo de victoria del juego
        
        Returns:
            str or None: "simple", "gammon", "backgammon" o None si no hay ganador
        """
        return self.__tipo_victoria__
    
    def get_puntos_victoria(self):
        """
        Retorna la cantidad de puntos obtenidos según el tipo de victoria
        
        Returns:
            int: 1 para simple, 2 para gammon, 3 para backgammon, 0 si no hay victoria
        """
        if self.__tipo_victoria__ == "simple":
            return 1
        elif self.__tipo_victoria__ == "gammon":
            return 2
        elif self.__tipo_victoria__ == "backgammon":
            return 3
        return 0
    
    def get_fichas_sacadas(self):
        """
        Retorna el contador de fichas sacadas por bear off para cada jugador
        
        Returns:
            dict: {"blanco": int, "negro": int}
        """
        return self.__fichas_sacadas__.copy()
    
    def reiniciar_juego(self):
        """
        Reinicia el juego a su estado inicial
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__turno_actual__ = self.__player1__
        self.__juego_terminado__ = False
        self.__ganador__ = None
        self.__tipo_victoria__ = None
        self.__fichas_sacadas__ = {"blanco": 0, "negro": 0}
    
    
        
       