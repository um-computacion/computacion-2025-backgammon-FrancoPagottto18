
"""
Interfaz de línea de comandos para Backgammon
"""

import sys
from backgammon.core.game import Game
from backgammon.core.exceptions import MovimientoInvalidoError, JuegoTerminadoError


class BackgammonCLI:
    """CLI para jugar Backgammon"""
    
    def __init__(self):
        self.__game__ = None
        self.__running__ = True
        self.__dados_disponibles__ = []
        self.__dados_usados__ = []

    def run(self):
        """Ejecuta el juego"""
        self._mostrar_inicio()
        
        while self.__running__:
            try:
                self._mostrar_menu()
                comando = input("\n> ").strip().lower()
                self._procesar_comando(comando)
                    
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def _mostrar_inicio(self):
        """Muestra mensaje de bienvenida"""
        print("=" * 60)
        print("🎲 BACKGAMMON 🎲".center(60))
        print("=" * 60)
        print("Objetivo: Llevar todas las fichas a casa".center(60))
        print("=" * 60)

    def _mostrar_menu(self):
        """Muestra el menú actual"""
        if self.__game__ and not self.__game__.juego_terminado():
            jugador = self.__game__.get_turno_actual()
            color = "⚪" if jugador.get_color() == "blanco" else "⚫"
            print(f"\n🎯 Turno: {jugador.get_name()} {color}")
            print("Comandos: nueva, tablero, dados, mover, pasar, ayuda, salir")
        else:
            print("\n📋 MENÚ:")
            print("1. nueva - Crear partida")
            print("2. ayuda - Ver ayuda")
            print("3. salir - Terminar")

    def _procesar_comando(self, comando):
        """Procesa comandos del usuario"""
        comandos = {
            'nueva': self._nueva_partida,
            'n': self._nueva_partida,
            '1': self._nueva_partida,
            'tablero': self._ver_tablero,
            't': self._ver_tablero,
            '2': self._ver_tablero,
            'dados': self._tirar_dados,
            'd': self._tirar_dados,
            '3': self._tirar_dados,
            'mover': self._mover_ficha,
            'm': self._mover_ficha,
            '4': self._mover_ficha,
            'pasar': self._cambiar_turno,
            'p': self._cambiar_turno,
            '5': self._cambiar_turno,
            'ayuda': self._mostrar_ayuda,
            'help': self._mostrar_ayuda,
            'h': self._mostrar_ayuda,
            '?': self._mostrar_ayuda,
            'salir': self._terminar,
            's': self._terminar,
            'exit': self._terminar,
            'q': self._terminar
        }
        
        if comando in comandos:
            comandos[comando]()
        elif comando == "":
            print("💡 Ingrese un comando")
        else:
            print(f"❌ Comando '{comando}' no válido")
            print("💡 Escriba 'ayuda' para ver comandos")

    def _nueva_partida(self):
        """Crea nueva partida"""
        print("\n🆕 NUEVA PARTIDA")
        
        try:
            print("📝 Nombres de jugadores:")
            nombre1 = input("   Jugador 1 (⚪ Blancas): ").strip()
            nombre2 = input("   Jugador 2 (⚫ Negras): ").strip()
            
            if not nombre1 or not nombre2:
                print("❌ Los nombres no pueden estar vacíos")
                return
                
            if nombre1 == nombre2:
                print("❌ Los nombres deben ser diferentes")
                return
                
            self.__game__ = Game(nombre1, nombre2)
            
            print(f"\n✅ ¡Partida creada!")
            print(f"   {nombre1} (⚪) vs {nombre2} (⚫)")
            print("💡 Use 'tablero' para ver el estado")
            
        except Exception as e:
            print(f"❌ Error: {e}")

    def _ver_tablero(self):
        """Muestra el tablero visual en ASCII"""
        if not self.__game__:
            print("❌ No hay partida. Use 'nueva' para iniciar.")
            return

        try:
            posiciones = self._obtener_posiciones()
            barra = self._obtener_barra()
            
            if not posiciones or len(posiciones) != 24:
                print("❌ Error: Estado del tablero inválido")
                return
                
            print("\n" + "="*80)
            print("                              TABLERO DE BACKGAMMON")
            print("="*80)
            
            # Fichas fuera
            print("Fichas fuera - Blancas: 0 | Negras: 0")
            print()
            
            # Parte superior del tablero (posiciones 13-24)
            self._mostrar_fila_superior(posiciones)
            
            # Barra central
            self._mostrar_barra(barra)
            
            # Parte inferior del tablero (posiciones 12-1)
            self._mostrar_fila_inferior(posiciones)
            
            print("="*80)
            
            # Mostrar turno actual
            jugador = self.__game__.get_turno_actual()
            color_symbol = "⚪" if jugador.get_color() == "blanco" else "⚫"
            print(f"🎯 TURNO ACTUAL: {jugador.get_name()} {color_symbol}")
            print()
            
        except Exception as e:
            print(f"❌ Error mostrando tablero: {e}")

    def _obtener_posiciones(self):
        """Obtiene las posiciones del tablero como lista de enteros"""
        if not self.__game__:
            return []
            
        puntos = self.__game__.get_board().get_puntos()
        posiciones = []
        
        for punto in puntos:
            if len(punto) == 0:
                posiciones.append(0)
            else:
                color = punto[0].get_color()
                cantidad = len(punto)
                if color == "blanco":
                    posiciones.append(cantidad)
                else:
                    posiciones.append(-cantidad)
        
        return posiciones

    def _obtener_barra(self):
        """Obtiene el estado de la barra"""
        if not self.__game__:
            return {"blancas": 0, "negras": 0}
            
        barra = self.__game__.get_board().get_barra()
        return {
            "blancas": len(barra.get("blanco", [])),
            "negras": len(barra.get("negro", []))
        }
    
    def _mostrar_fila_superior(self, posiciones):
        """Muestra la fila superior del tablero (13-24)"""
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Números de posición (13-24)
        numeros = "│"
        for i in range(13, 19):  # 13-18
            numeros += f" {i:2d}  │"
        numeros += "   │"  # Separador
        for i in range(19, 25):  # 19-24
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Fichas (máximo 5 filas visibles)
        for fila in range(5):
            linea = "│"
            
            # Posiciones 13-18
            for posicion in range(13, 19):
                idx = posicion - 1  # Convertir a índice 0-based
                
                if idx >= len(posiciones):
                    fichas = 0
                else:
                    fichas = posiciones[idx]
                
                # Mostrar ficha si existe en esta fila
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
            
            # Separador en el medio
            linea += "   │"
            
            # Posiciones 19-24
            for posicion in range(19, 25):
                idx = posicion - 1  # Convertir a índice 0-based
                
                if idx >= len(posiciones):
                    fichas = 0
                else:
                    fichas = posiciones[idx]
                
                # Mostrar ficha si existe en esta fila
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
            
            print(linea)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")
    
    def _mostrar_barra(self, barra):
        """Muestra la barra central"""
        try:
            blancas_barra = barra.get('blancas', 0)
            negras_barra = barra.get('negras', 0)
            print(f"                                 BARRA")
            print(f"                        Blancas: {blancas_barra} | Negras: {negras_barra}")
            print()
        except Exception as e:
            print(f"                        Error mostrando barra: {e}")
            print()
    
    def _mostrar_fila_inferior(self, posiciones):
        """Muestra la fila inferior del tablero (12-1)"""
        print("┌─────┬─────┬─────┬─────┬─────┬─────┬───┬─────┬─────┬─────┬─────┬─────┬─────┐")
        
        # Fichas (máximo 5 filas visibles, de arriba hacia abajo)
        for fila in range(4, -1, -1):
            linea = "│"
            
            # Posiciones 12-7
            for posicion in range(12, 6, -1):
                idx = posicion - 1  # Convertir a índice 0-based
                
                if idx >= len(posiciones) or idx < 0:
                    fichas = 0
                else:
                    fichas = posiciones[idx]
                
                # Mostrar ficha si existe en esta fila
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
            
            # Separador en el medio
            linea += "   │"
            
            # Posiciones 6-1
            for posicion in range(6, 0, -1):
                idx = posicion - 1  # Convertir a índice 0-based
                
                if idx >= len(posiciones) or idx < 0:
                    fichas = 0
                else:
                    fichas = posiciones[idx]
                
                # Mostrar ficha si existe en esta fila
                if abs(fichas) > fila:
                    if fichas > 0:
                        linea += "  B  │"  # Blanca
                    else:
                        linea += "  N  │"  # Negra
                else:
                    linea += "     │"
            
            print(linea)
        
        print("├─────┼─────┼─────┼─────┼─────┼─────┼───┼─────┼─────┼─────┼─────┼─────┼─────┤")
        
        # Números de posición (12-1)
        numeros = "│"
        for i in range(12, 6, -1):  # 12-7
            numeros += f" {i:2d}  │"
        numeros += "   │"  # Separador
        for i in range(6, 0, -1):  # 6-1
            numeros += f" {i:2d}  │"
        print(numeros)
        
        print("└─────┴─────┴─────┴─────┴─────┴─────┴───┴─────┴─────┴─────┴─────┴─────┴─────┘")

    def _tirar_dados(self):
        """Tira los dados"""
        if not self.__game__:
            print("❌ No hay partida. Use 'nueva' para iniciar.")
            return
            
        try:
            valores = self.__game__.tirar_dados()
            self.__dados_disponibles__ = valores.copy()
            self.__dados_usados__ = []
            
            print(f"\n🎲 Dados: {valores}")
            
            if self.__game__.get_dice().es_doble():
                print("¡Doble! 4 movimientos disponibles")
            else:
                print("2 movimientos disponibles")
            
            print(f"Dados disponibles: {self.__dados_disponibles__}")
                
        except JuegoTerminadoError:
            print("❌ El juego terminó")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _mover_ficha(self):
        """Mueve una ficha"""
        if not self.__game__:
            print("❌ No hay partida. Use 'nueva' para iniciar.")
            return
            
        # Verificar si hay dados disponibles
        if not self.__dados_disponibles__:
            print("❌ No hay dados disponibles. Use 'dados' para tirar primero.")
            return
            
        try:
            print("\n📍 MOVER FICHA")
            print(f"Dados disponibles: {self.__dados_disponibles__}")
            
            desde = input("Desde (1-24, -1 para barra): ").strip()
            hacia = input("Hacia (1-24, -1 para sacar): ").strip()
            
            desde = int(desde) if desde else 0
            hacia = int(hacia) if hacia else 0
            
            # Convertir a índices 0-based
            desde_idx = desde - 1 if desde > 0 else -1
            hacia_idx = hacia - 1 if hacia > 0 else -1
            
            # Calcular distancia del movimiento
            if desde_idx != -1 and hacia_idx != -1:
                distancia = abs(hacia_idx - desde_idx)
            elif desde_idx == -1:  # Desde barra
                if hacia_idx != -1:
                    distancia = hacia_idx + 1 if self.__game__.get_turno_actual().get_color() == "blanco" else 24 - hacia_idx
                else:
                    distancia = 0
            else:  # Bear off
                distancia = desde_idx + 1 if self.__game__.get_turno_actual().get_color() == "negro" else 24 - desde_idx
            
            # Verificar si la distancia coincide con algún dado disponible
            if distancia not in self.__dados_disponibles__:
                print(f"❌ Movimiento inválido: distancia {distancia} no coincide con dados disponibles {self.__dados_disponibles__}")
                return
            
            # Realizar el movimiento
            self.__game__.mover_ficha(desde_idx, hacia_idx)
            
            # Usar el dado correspondiente
            self.__dados_disponibles__.remove(distancia)
            self.__dados_usados__.append(distancia)
            
            print(f"✅ Ficha movida (usado dado: {distancia})")
            print(f"Dados restantes: {self.__dados_disponibles__}")
            
            # Verificar si se acabaron los dados
            if not self.__dados_disponibles__:
                print("🎯 Todos los dados utilizados. Use 'pasar' para cambiar turno.")
            
            # Verificar ganador
            if self.__game__.juego_terminado():
                ganador = self.__game__.get_ganador()
                print(f"\n🏆 ¡JUEGO TERMINADO! Ganador: {ganador.get_name()}")
                
        except ValueError:
            print("❌ Ingrese números válidos")
        except MovimientoInvalidoError as e:
            print(f"❌ Movimiento inválido: {e}")
        except JuegoTerminadoError:
            print("❌ El juego terminó")
        except Exception as e:
            print(f"❌ Error: {e}")

    def _cambiar_turno(self):
        """Cambia el turno"""
        if not self.__game__:
            print("❌ No hay partida. Use 'nueva' para iniciar.")
            return
            
        try:
            # Limpiar dados del turno anterior
            self.__dados_disponibles__ = []
            self.__dados_usados__ = []
            
            jugador_anterior = self.__game__.get_turno_actual()
            self.__game__.cambiar_turno()
            jugador_nuevo = self.__game__.get_turno_actual()
            
            print(f"\n✅ Turno: {jugador_anterior.get_name()} → {jugador_nuevo.get_name()}")
            print("💡 Use 'dados' para tirar los dados del nuevo turno")
            
        except Exception as e:
            print(f"❌ Error: {e}")

    def _mostrar_ayuda(self):
        """Muestra ayuda"""
        print("\n" + "=" * 50)
        print("AYUDA - BACKGAMMON".center(50))
        print("=" * 50)
        
        print("\n🎮 COMANDOS:")
        print("   nueva    - Crear partida")
        print("   tablero  - Ver tablero")
        print("   dados    - Tirar dados")
        print("   mover    - Mover ficha")
        print("   pasar    - Cambiar turno")
        print("   ayuda    - Ver ayuda")
        print("   salir    - Terminar")
        
        print("\n🎯 CÓMO JUGAR:")
        print("   1. Use 'nueva' para crear partida")
        print("   2. Use 'dados' para tirar")
        print("   3. Use 'mover' para mover fichas (debe coincidir con dados)")
        print("   4. Use 'pasar' para cambiar turno")
        
        print("\n📋 REGLAS:")
        print("   • ⚪ Blancas van del 24 al 1")
        print("   • ⚫ Negras van del 1 al 24")
        print("   • Cada jugador tiene 15 fichas")
        print("   • Los dados LIMITAN cuánto mover")
        print("   • Debe usar exactamente los valores de los dados")
        print("   • Gana quien lleve todas a casa")
        
        print("\n" + "=" * 50)

    def _terminar(self):
        """Termina el juego"""
        print("\n🎉 ¡Gracias por jugar!")
        print("👋 ¡Hasta la próxima!")
        self.__running__ = False


def main():
    """Función principal"""
    cli = BackgammonCLI()
    cli.run()


if __name__ == "__main__":
    main()