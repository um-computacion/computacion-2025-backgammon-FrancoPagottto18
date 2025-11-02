#!/usr/bin/env python3
"""
Interfaz gráfica de Backgammon usando Pygame
Adaptado del código del profesor manteniendo la lógica de movimientos existente
"""

import pygame
from backgammon.core.game import Game
from backgammon.core.exceptions import MovimientoInvalidoError, JuegoTerminadoError

# ------------------ Config visual ------------------
WIDTH, HEIGHT = 1300, 700  # Ventana más ancha para área de fichas guardadas
MARGIN_X, MARGIN_Y = 40, 40
SAVED_AREA_WIDTH = 250  # Ancho del área de fichas guardadas
BG_COLOR = (245, 239, 230)
BOARD_COLOR = (230, 220, 200)
TRI_A = (170, 120, 90)
TRI_B = (210, 170, 130)
LINE = (60, 60, 60)
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
TEXT = (25, 25, 25)
HIGHLIGHT_COLOR = (255, 255, 0) # Amarillo para selección

MAX_VISIBLE_STACK = 5  # como la CLI


def point_index_to_display(idx):
    """
    idx 0..23 (nuestro board.__puntos__)
    Retorna: row ('top'|'bottom') y columna visual 0..11
    - 0..11 (superior): se muestran como 12..1; col_vis = 11-idx
    - 12..23 (inferior): col_vis = idx - 12
    """
    if 0 <= idx <= 11:
        return 'top', 11 - idx
    else:
        return 'bottom', idx - 12


def draw_triangle(surface, board_rect, col_vis, row, color):
    x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
    x1 = x0 + (board_rect.width / 12.0)
    x_mid = (x0 + x1) / 2.0

    if row == 'top':
        tip_y = board_rect.top + board_rect.height * 0.42
        pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
    else:
        tip_y = board_rect.bottom - board_rect.height * 0.42
        pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
    pygame.draw.polygon(surface, color, pts)


def draw_checker(surface, center, radius, color_rgb, label=None, font=None):
    pygame.draw.circle(surface, color_rgb, center, radius)
    pygame.draw.circle(surface, LINE, center, radius, 1)
    if label and font:
        txt = font.render(str(label), True, LINE if color_rgb == WHITE else WHITE)
        rect = txt.get_rect(center=center)
        surface.blit(txt, rect)


class BoardAdapter:
    """
    Adaptador para convertir la estructura del Board a la que espera el código visual
    """
    
    def __init__(self, game):
        self.__game__ = game
    
    @property
    def pos(self):
        """
        Convierte __puntos__ (listas de Checker) a formato esperado (tuplas con color y cantidad)
        """
        result = {}
        board = self.__game__.get_board()
        puntos = board.get_puntos()
        
        for i, punto in enumerate(puntos):
            if punto:  # Si hay fichas en este punto
                color = punto[0].get_color()  # Color de la primera ficha
                count = len(punto)
                # Convertir "blanco"/"negro" a "white"/"black"
                color_name = "white" if color == "blanco" else "black"
                result[i] = (color_name, count)
        return result


def draw_saved_checkers_area(surface, game, font):
    """
    Dibuja el área a la derecha donde se muestran las fichas guardadas (bear off)
    Retorna los rectángulos clickeables para blancas y negras
    """
    # Área de fichas guardadas
    saved_rect = pygame.Rect(
        WIDTH - SAVED_AREA_WIDTH - 10,
        MARGIN_Y + 20,
        SAVED_AREA_WIDTH,
        HEIGHT - 2 * MARGIN_Y - 40
    )
    
    # Fondo del área
    pygame.draw.rect(surface, BOARD_COLOR, saved_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, saved_rect, 2, border_radius=12)
    
    # Título
    title_font = pygame.font.SysFont(None, 28, bold=True)
    title = title_font.render("Fichas Guardadas", True, TEXT)
    title_rect = title.get_rect(centerx=saved_rect.centerx, top=saved_rect.top + 15)
    surface.blit(title, title_rect)
    
    # Obtener fichas sacadas
    fichas_sacadas = game.get_fichas_sacadas()
    blancas_sacadas = fichas_sacadas.get("blanco", 0)
    negras_sacadas = fichas_sacadas.get("negro", 0)
    
    # Tamaño de las fichas en el área guardada
    checker_radius = 18
    checker_spacing = 25
    
    # Dividir el área en dos secciones iguales
    section_height = (saved_rect.height - 60) // 2  # 60 para título y espaciado
    
    # Área para fichas blancas (parte superior) - clickeable
    white_area_top = saved_rect.top + 60
    white_area_bottom = white_area_top + section_height - 20
    white_area_y = white_area_top + 30
    white_area_rect = pygame.Rect(
        saved_rect.left + 10,
        white_area_top,
        saved_rect.width - 20,
        section_height - 20
    )
    
    white_label = font.render(f"Blancas: {blancas_sacadas}", True, TEXT)
    white_label_rect = white_label.get_rect(centerx=saved_rect.centerx, top=white_area_top + 5)
    surface.blit(white_label, white_label_rect)
    
    # Dibujar fichas blancas guardadas (máximo 5 por fila)
    if blancas_sacadas > 0:
        cols_per_row = 5
        max_cols = min(cols_per_row, blancas_sacadas)
        total_width = (max_cols - 1) * checker_spacing
        start_x = saved_rect.centerx - total_width / 2
        
        for i in range(min(blancas_sacadas, 30)):  # Máximo 30 fichas visibles (6 filas x 5)
            row = i // cols_per_row
            col = i % cols_per_row
            x = start_x + col * checker_spacing
            y = white_area_y + row * checker_spacing
            if y + checker_radius < white_area_bottom:
                draw_checker(surface, (int(x), int(y)), checker_radius, WHITE, None, font)
    
    # Área para fichas negras (parte inferior) - clickeable
    black_area_top = saved_rect.centery + 10
    black_area_bottom = saved_rect.bottom - 20
    black_area_y = black_area_top + 30
    black_area_rect = pygame.Rect(
        saved_rect.left + 10,
        black_area_top,
        saved_rect.width - 20,
        section_height
    )
    
    black_label = font.render(f"Negras: {negras_sacadas}", True, TEXT)
    black_label_rect = black_label.get_rect(centerx=saved_rect.centerx, top=black_area_top + 5)
    surface.blit(black_label, black_label_rect)
    
    # Dibujar fichas negras guardadas (máximo 5 por fila)
    if negras_sacadas > 0:
        cols_per_row = 5
        max_cols = min(cols_per_row, negras_sacadas)
        total_width = (max_cols - 1) * checker_spacing
        start_x = saved_rect.centerx - total_width / 2
        
        for i in range(min(negras_sacadas, 30)):  # Máximo 30 fichas visibles (6 filas x 5)
            row = i // cols_per_row
            col = i % cols_per_row
            x = start_x + col * checker_spacing
            y = black_area_y + row * checker_spacing
            if y + checker_radius < black_area_bottom:
                draw_checker(surface, (int(x), int(y)), checker_radius, BLACK, None, font)
    
    # Retornar los rectángulos clickeables
    # -2 para área de guardado blanco, -3 para área de guardado negro
    return {
        -2: white_area_rect,  # Área clickeable para guardar fichas blancas
        -3: black_area_rect   # Área clickeable para guardar fichas negras
    }


def render_board(surface, game, font, selected_point=None):
    """
    Dibuja el tablero y devuelve un hitmap:
    hitmap: dict[int -> list[(center_x, center_y, radius)]]
    """
    surface.fill(BG_COLOR)

    # Marco del tablero (dejando espacio para el área de fichas guardadas)
    board_rect = pygame.Rect(
        MARGIN_X,
        MARGIN_Y + 20,
        WIDTH - 2 * MARGIN_X - SAVED_AREA_WIDTH - 20,  # Reducir ancho para dejar espacio
        HEIGHT - 2 * MARGIN_Y - 40
    )
    pygame.draw.rect(surface, BOARD_COLOR, board_rect, border_radius=12)
    pygame.draw.rect(surface, LINE, board_rect, 2, border_radius=12)

    # Triángulos (alternados)
    for col_vis in range(12):
        draw_triangle(surface, board_rect, col_vis, 'top', TRI_A if col_vis % 2 == 0 else TRI_B)
        draw_triangle(surface, board_rect, col_vis, 'bottom', TRI_B if col_vis % 2 == 0 else TRI_A)

    # Parámetros para fichas
    tri_w = board_rect.width / 12.0
    radius = int(tri_w * 0.38)
    radius = max(12, min(radius, 22))
    vgap = 4  # separación vertical entre fichas
    step = radius * 2 + vgap

    # Etiquetas de puntos (top: 12..1, bottom: 13..24)
    top_labels = [str(i) for i in range(12, 0, -1)]
    for col_vis, lbl in enumerate(top_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.top - 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    bottom_labels = [str(i) for i in range(13, 25)]
    for col_vis, lbl in enumerate(bottom_labels):
        x = int(board_rect.left + col_vis * tri_w + tri_w / 2)
        y = board_rect.bottom + 14
        img = font.render(lbl, True, TEXT)
        rect = img.get_rect(center=(x, y))
        surface.blit(img, rect)

    # Barra central para fichas capturadas
    barra_rect = pygame.Rect(
        board_rect.centerx - 120,
        board_rect.centery - 40,
        240,
        80
    )
    pygame.draw.rect(surface, BOARD_COLOR, barra_rect, border_radius=8)
    pygame.draw.rect(surface, LINE, barra_rect, 3, border_radius=8)
    
    # Dibujar fichas en la barra
    barra = game.get_board().get_barra()
    blancas_capturadas = len(barra["blanco"])
    negras_capturadas = len(barra["negro"])
    
    # Lado izquierdo: fichas blancas capturadas
    if blancas_capturadas > 0:
        white_x = barra_rect.left + 20
        white_y = barra_rect.centery
        for i in range(min(blancas_capturadas, 10)):
            offset_x = i % 5 * 15
            offset_y = (i // 5) * 30
            draw_checker(surface, (white_x + offset_x, white_y + offset_y - 15), 10, WHITE, None, font)
    
    # Lado derecho: fichas negras capturadas
    if negras_capturadas > 0:
        black_x = barra_rect.right - 20
        black_y = barra_rect.centery
        for i in range(min(negras_capturadas, 10)):
            offset_x = -(i % 5) * 15
            offset_y = (i // 5) * 30
            draw_checker(surface, (black_x + offset_x, black_y + offset_y - 15), 10, BLACK, None, font)
    
    # Etiquetas
    if blancas_capturadas > 0:
        text = font.render(f"Blancas: {blancas_capturadas}", True, TEXT)
        surface.blit(text, (barra_rect.left + 5, barra_rect.top + 5))
    
    if negras_capturadas > 0:
        text = font.render(f"Negras: {negras_capturadas}", True, TEXT)
        text_rect = text.get_rect()
        text_rect.right = barra_rect.right - 5
        text_rect.top = barra_rect.top + 5
        surface.blit(text, text_rect)

    # --- H I T M A P  (centros de fichas por punto) ---
    hitmap = {i: [] for i in range(24)}
    
    # Agregar barra al hitmap (índice -1 para representar la barra)
    hitmap[-1] = [(barra_rect.centerx, barra_rect.centery, 120, 'circle')]  # x, y, radio, tipo

    # Crear adaptador del tablero
    board_adapter = BoardAdapter(game)
    pos_data = board_adapter.pos

    # Dibujar fichas según pos_data y crear hitmap para TODOS los puntos
    for idx in range(24):
        row, col_vis = point_index_to_display(idx)
        cx = int(board_rect.left + col_vis * tri_w + tri_w / 2)

        # Resaltar punto seleccionado
        if selected_point == idx:
            # Dibujar borde de selección
            if row == 'top':
                tip_y = board_rect.top + board_rect.height * 0.42
                x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
                x1 = x0 + (board_rect.width / 12.0)
                x_mid = (x0 + x1) / 2.0
                pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
            else:
                tip_y = board_rect.bottom - board_rect.height * 0.42
                x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
                x1 = x0 + (board_rect.width / 12.0)
                x_mid = (x0 + x1) / 2.0
                pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
            pygame.draw.polygon(surface, HIGHLIGHT_COLOR, pts, 3)

        # Dibujar fichas si las hay
        if idx in pos_data:
            cell = pos_data[idx]
            color_name, count = cell
            
            if row == 'top':
                start_y = int(board_rect.top + radius + 6)
                visibles = min(count, MAX_VISIBLE_STACK)
                extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0
                for i in range(visibles):
                    cy = start_y + i * step
                    label = extras if (extras and i == visibles - 1) else None
                    draw_checker(surface, (cx, cy), radius, WHITE if color_name == 'white' else BLACK, label, font)
                    hitmap[idx].append((cx, cy, radius))
            else:
                start_y = int(board_rect.bottom - radius - 6)
                visibles = min(count, MAX_VISIBLE_STACK)
                extras = max(0, count - (MAX_VISIBLE_STACK - 1)) if count > MAX_VISIBLE_STACK else 0
                for i in range(visibles):
                    cy = start_y - i * step
                    label = extras if (extras and i == visibles - 1) else None
                    draw_checker(surface, (cx, cy), radius, WHITE if color_name == 'white' else BLACK, label, font)
                    hitmap[idx].append((cx, cy, radius))
        else:
            # Punto vacío: crear área de click que cubre todo el triángulo
            if row == 'top':
                tip_y = board_rect.top + board_rect.height * 0.42
                x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
                x1 = x0 + (board_rect.width / 12.0)
                x_mid = (x0 + x1) / 2.0
                pts = [(x0, board_rect.top), (x1, board_rect.top), (x_mid, tip_y)]
            else:
                tip_y = board_rect.bottom - board_rect.height * 0.42
                x0 = board_rect.left + col_vis * (board_rect.width / 12.0)
                x1 = x0 + (board_rect.width / 12.0)
                x_mid = (x0 + x1) / 2.0
                pts = [(x0, board_rect.bottom), (x1, board_rect.bottom), (x_mid, tip_y)]
            # Guardar triángulo en hitmap: (v0, v1, v2, 'triangle')
            hitmap[idx].append((pts[0], pts[1], pts[2], 'triangle'))

    # Dibujar área de fichas guardadas y obtener rectángulos clickeables
    saved_areas = draw_saved_checkers_area(surface, game, font)
    
    # Agregar áreas de guardado al hitmap (-2 para blancas, -3 para negras)
    for area_idx, area_rect in saved_areas.items():
        hitmap[area_idx] = [area_rect]  # Guardar el rectángulo completo

    return hitmap


def point_in_triangle(pt, v0, v1, v2):
    """Verifica si un punto está dentro de un triángulo (usando producto vectorial)"""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(pt, v0, v1)
    d2 = sign(pt, v1, v2)
    d3 = sign(pt, v2, v0)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)


def hit_test(hitmap, pos):
    """ Devuelve el índice de punto (0..23, -1 barra, -2 guardado blanco, -3 guardado negro) si el click cae en alguna ficha; si no, None. """
    mx, my = pos

    # Priorizar áreas de guardado (-2, -3) primero si existen
    if -2 in hitmap:
        for shape in hitmap[-2]:
            # Verificar si es un rectángulo (pygame.Rect tiene método collidepoint)
            if hasattr(shape, 'collidepoint'):
                if shape.collidepoint(pos):
                    return -2
    if -3 in hitmap:
        for shape in hitmap[-3]:
            # Verificar si es un rectángulo (pygame.Rect tiene método collidepoint)
            if hasattr(shape, 'collidepoint'):
                if shape.collidepoint(pos):
                    return -3

    # Recorremos todos los círculos; si hay solapados, el primero que matchee corta.
    for idx, shapes in hitmap.items():
        # Saltar áreas de guardado ya procesadas
        if idx in (-2, -3):
            continue
        for shape in shapes:
            # Verificar si es un rectángulo (pygame.Rect tiene método collidepoint)
            if hasattr(shape, 'collidepoint'):
                # Rectángulo: área clickeable
                if shape.collidepoint(pos):
                    return idx
            elif len(shape) == 3:
                # Círculo: (cx, cy, r)
                cx, cy, r = shape
                dx, dy = mx - cx, my - cy
                if dx*dx + dy*dy <= r*r:
                    return idx
            elif len(shape) == 4:
                if shape[3] == 'triangle':
                    # Triángulo: (v0, v1, v2, 'triangle')
                    v0, v1, v2 = shape[0], shape[1], shape[2]
                    if point_in_triangle(pos, v0, v1, v2):
                        return idx
                elif shape[3] == 'circle':
                    # Círculo con radio: (cx, cy, r, 'circle')
                    cx, cy, r = shape[0], shape[1], shape[2]
                    dx, dy = mx - cx, my - cy
                    if dx*dx + dy*dy <= r*r:
                        return idx
    return None


def main():
    pygame.init()
    pygame.display.set_caption("Backgammon (Pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)

    # Nuestro juego
    game = Game("Jugador Blanco", "Jugador Negro")
    print("Juego inicializado correctamente")
    print("Controles:")
    print("- ESPACIO: Tirar dados")
    print("- Click: Seleccionar punto origen y destino")
    print("- ESC/Q: Salir")

    # Estado del juego
    selected_point = None
    dados_tirados = False
    movimientos_realizados = 0
    movimientos_requeridos = 0
    dados_disponibles = []
    mensaje_error = None
    tiempo_error = 0
    mensaje_victoria = None  # Mensaje persistente de victoria

    running = True
    # Inicializar hitmap vacío
    hitmap = {}
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif e.key == pygame.K_SPACE:
                    if not dados_tirados:
                        game.tirar_dados()
                        dados_tirados = True
                        dados_raw = game.get_dice().get_valores()
                        dados_disponibles = list(dados_raw) # Copia para poder modificar
                        movimientos_requeridos = len(dados_disponibles)
                        movimientos_realizados = 0
                        print(f"Dados tirados: {dados_raw}")
                    else:
                        print(f"Debes usar todos los dados antes de tirar de nuevo ({movimientos_realizados}/{movimientos_requeridos})")
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if not dados_tirados:
                    print("Primero debes tirar los dados (presiona ESPACIO)")
                    continue
                
                # Verificar si se clickeó el botón "Pasar"
                button_width = 120
                button_height = 40
                button_x = WIDTH - SAVED_AREA_WIDTH - button_width - 30  # Evitar superposición con área guardada
                button_y = 10
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                
                if button_rect.collidepoint(e.pos):
                    print("Botón PASAR presionado")
                    game.cambiar_turno()
                    dados_tirados = False
                    movimientos_realizados = 0
                    movimientos_requeridos = 0
                    dados_disponibles = []
                    selected_point = None
                    print(f"Turno de: {game.get_turno_actual().get_name()}")
                    continue
                    
                idx = hit_test(hitmap, e.pos)
                if idx is not None:
                    # Manejar clicks en áreas de guardado (-2 para blancas, -3 para negras)
                    if idx == -2 or idx == -3:
                        turno_actual = game.get_turno_actual().get_color()
                        color_guardado = "blanco" if idx == -2 else "negro"
                        
                        # Verificar que sea el turno del jugador correcto
                        if turno_actual != color_guardado:
                            mensaje_error = f"No es tu turno para guardar fichas {color_guardado}"
                            tiempo_error = pygame.time.get_ticks()
                            print(mensaje_error)
                            continue
                        
                        # Si hay un punto seleccionado, intentar guardar la ficha
                        if selected_point is not None and selected_point >= 0:
                            try:
                                # Verificar que puede hacer bear off
                                if not game._puede_hacer_bear_off(turno_actual):
                                    mensaje_error = "Solo puedes guardar fichas cuando todas están en tu cuadrante de casa"
                                    tiempo_error = pygame.time.get_ticks()
                                    print(mensaje_error)
                                    selected_point = None
                                    continue
                                
                                # Calcular distancia para bear off
                                distancia = game._calcular_distancia(selected_point, -1, turno_actual)
                                
                                # Buscar un dado que sea mayor o igual a la distancia (en bear off se puede usar un dado mayor)
                                dado_usado = None
                                # Buscar primero uno exacto, luego el menor que sea >= distancia
                                dado_exacto = None
                                dado_minimo = None
                                for i, valor_dado in enumerate(dados_disponibles):
                                    if valor_dado == distancia:
                                        dado_exacto = (i, valor_dado)
                                        break
                                    elif valor_dado >= distancia:
                                        if dado_minimo is None or valor_dado < dado_minimo[1]:
                                            dado_minimo = (i, valor_dado)
                                
                                if dado_exacto:
                                    idx_dado, valor_dado = dado_exacto
                                    dado_usado = valor_dado
                                    dados_disponibles.pop(idx_dado)
                                elif dado_minimo:
                                    idx_dado, valor_dado = dado_minimo
                                    dado_usado = valor_dado
                                    dados_disponibles.pop(idx_dado)
                                
                                if dado_usado is None:
                                    mensaje_error = f"No tienes un dado mayor o igual a {distancia} para guardar esta ficha"
                                    tiempo_error = pygame.time.get_ticks()
                                    print(mensaje_error)
                                    selected_point = None
                                    continue
                                
                                # Realizar el movimiento bear off
                                game.mover_ficha(selected_point, -1, dado_usado)
                                movimientos_realizados += 1
                                origen_str = str(selected_point + 1)
                                print(f"Ficha guardada desde punto {origen_str} usando dado {dado_usado} ({movimientos_realizados}/{movimientos_requeridos})")
                                
                                # Verificar si hay un ganador después del movimiento
                                if game.juego_terminado():
                                    ganador = game.get_ganador()
                                    tipo_victoria = game.get_tipo_victoria()
                                    puntos = game.get_puntos_victoria()
                                    color_ganador = ganador.get_color()
                                    
                                    mensaje_victoria = f"¡Felicitaciones ganador ({color_ganador})!"
                                    
                                    print(f"\n🏆 {mensaje_victoria}")
                                    print("¡Juego terminado!")
                                
                                # Verificar si se han usado todos los dados
                                if movimientos_realizados >= movimientos_requeridos and not game.juego_terminado():
                                    print("¡Turno completado! Cambiando turno...")
                                    game.cambiar_turno()
                                    dados_tirados = False
                                    movimientos_realizados = 0
                                    movimientos_requeridos = 0
                                    dados_disponibles = []
                                    print(f"Turno de: {game.get_turno_actual().get_name()}")
                                elif movimientos_realizados >= movimientos_requeridos and game.juego_terminado():
                                    dados_tirados = False
                                    movimientos_realizados = 0
                                    movimientos_requeridos = 0
                                    dados_disponibles = []
                                    
                            except MovimientoInvalidoError as ex:
                                mensaje_error = str(ex)
                                tiempo_error = pygame.time.get_ticks()
                                print(f"Movimiento inválido: {ex}")
                            except JuegoTerminadoError as ex:
                                print(f"Juego terminado: {ex}")
                                running = False
                            except Exception as ex:
                                mensaje_error = f"Error inesperado: {ex}"
                                tiempo_error = pygame.time.get_ticks()
                                print(mensaje_error)
                            finally:
                                selected_point = None
                        else:
                            # No hay punto seleccionado, solo mostrar mensaje informativo
                            if selected_point is None:
                                mensaje_error = "Primero selecciona una ficha para guardar"
                                tiempo_error = pygame.time.get_ticks()
                                print(mensaje_error)
                        continue
                    
                    punto_str = "barra" if idx == -1 else f"punto {idx + 1}"
                    print(f"Click en {punto_str}")
                    
                    if selected_point is None:
                        # Seleccionar punto origen
                        # Verificar si hay fichas en la barra que deben ser sacadas primero
                        turno_actual = game.get_turno_actual().get_color()
                        barra = game.get_board().get_barra()
                        fichas_en_barra = len(barra[turno_actual])
                        
                        # Si hay fichas en la barra, solo se puede seleccionar la barra (-1)
                        if fichas_en_barra > 0 and idx != -1:
                            mensaje_error = f"Tienes {fichas_en_barra} ficha(s) en la barra. Debes sacarlas primero."
                            tiempo_error = pygame.time.get_ticks()
                            print(mensaje_error)
                            continue
                        
                        # Si no hay fichas en la barra, verificar si se puede hacer bear off
                        if fichas_en_barra == 0 and idx == -1:
                            # Permitir seleccionar la barra solo si se puede hacer bear off
                            if not game._puede_hacer_bear_off(turno_actual):
                                mensaje_error = "No tienes fichas en la barra"
                                tiempo_error = pygame.time.get_ticks()
                                print(mensaje_error)
                                continue
                        
                        selected_point = idx
                        if idx == -1:
                            print(f"Seleccionado punto origen: BARRA")
                        else:
                            print(f"Seleccionado punto origen: {idx + 1}")
                    else:
                        # Si se hace click en el mismo punto, cancelar selección
                        if selected_point == idx:
                            print("Selección cancelada")
                            selected_point = None
                        else:
                            # Intentar mover ficha
                            try:
                                # Calcular la distancia del movimiento usando la dirección correcta
                                turno_actual = game.get_turno_actual().get_color()
                                
                                # Caso especial: mover desde la barra
                                if selected_point == -1:
                                    # Desde la barra: no permitir seleccionar la barra como destino (para reintroducir)
                                    if idx == -1:
                                        mensaje_error = "Selecciona un punto del tablero para sacar la ficha de la barra"
                                        tiempo_error = pygame.time.get_ticks()
                                        print(mensaje_error)
                                        selected_point = None
                                        continue
                                    # Calcular distancia desde la barra usando la lógica del juego
                                    # El juego calculará automáticamente la distancia correcta
                                    distancia = game._calcular_distancia(selected_point, idx, turno_actual)
                                # Caso especial: bear off (mover a la barra como destino)
                                elif idx == -1:
                                    # Movimiento bear off: sacar ficha del tablero
                                    # Calcular distancia usando la lógica del juego
                                    distancia = game._calcular_distancia(selected_point, -1, turno_actual)
                                    # Para bear off, buscar un dado mayor o igual
                                    dado_usado = None
                                    dado_exacto = None
                                    dado_minimo = None
                                    for i, valor_dado in enumerate(dados_disponibles):
                                        if valor_dado == distancia:
                                            dado_exacto = (i, valor_dado)
                                            break
                                        elif valor_dado >= distancia:
                                            if dado_minimo is None or valor_dado < dado_minimo[1]:
                                                dado_minimo = (i, valor_dado)
                                    
                                    if dado_exacto:
                                        idx_dado, valor_dado = dado_exacto
                                        dado_usado = valor_dado
                                        dados_disponibles.pop(idx_dado)
                                    elif dado_minimo:
                                        idx_dado, valor_dado = dado_minimo
                                        dado_usado = valor_dado
                                        dados_disponibles.pop(idx_dado)
                                    
                                    if dado_usado is None:
                                        mensaje_error = f"No tienes un dado mayor o igual a {distancia} para guardar esta ficha"
                                        tiempo_error = pygame.time.get_ticks()
                                        print(mensaje_error)
                                        selected_point = None
                                        continue
                                    
                                    # Realizar el movimiento bear off
                                    game.mover_ficha(selected_point, -1, dado_usado)
                                    movimientos_realizados += 1
                                    origen_str = str(selected_point + 1)
                                    print(f"Ficha guardada desde punto {origen_str} usando dado {dado_usado} ({movimientos_realizados}/{movimientos_requeridos})")
                                    
                                    # Verificar si hay un ganador después del movimiento
                                    if game.juego_terminado():
                                        ganador = game.get_ganador()
                                        tipo_victoria = game.get_tipo_victoria()
                                        puntos = game.get_puntos_victoria()
                                        color_ganador = ganador.get_color()
                                        
                                        mensaje_victoria = f"¡Felicitaciones ganador ({color_ganador})!"
                                        
                                        print(f"\n🏆 {mensaje_victoria}")
                                        print("¡Juego terminado!")
                                    
                                    # Verificar si se han usado todos los dados
                                    if movimientos_realizados >= movimientos_requeridos and not game.juego_terminado():
                                        print("¡Turno completado! Cambiando turno...")
                                        game.cambiar_turno()
                                        dados_tirados = False
                                        movimientos_realizados = 0
                                        movimientos_requeridos = 0
                                        dados_disponibles = []
                                        print(f"Turno de: {game.get_turno_actual().get_name()}")
                                    elif movimientos_realizados >= movimientos_requeridos and game.juego_terminado():
                                        dados_tirados = False
                                        movimientos_realizados = 0
                                        movimientos_requeridos = 0
                                        dados_disponibles = []
                                    
                                    selected_point = None
                                    continue
                                elif turno_actual == "blanco":
                                    # Blanco va de índice alto a bajo (23->0)
                                    if idx > selected_point:
                                        mensaje_error = "No puedes retroceder"
                                        tiempo_error = pygame.time.get_ticks()
                                        print(mensaje_error)
                                        selected_point = None
                                        continue
                                    distancia = selected_point - idx
                                else:
                                    # Negro va de índice bajo a alto (0->23)
                                    if idx < selected_point:
                                        mensaje_error = "No puedes retroceder"
                                        tiempo_error = pygame.time.get_ticks()
                                        print(mensaje_error)
                                        selected_point = None
                                        continue
                                    distancia = idx - selected_point
                                
                                # Buscar un dado que coincida con la distancia
                                dado_usado = None
                                for i, valor_dado in enumerate(dados_disponibles):
                                    if valor_dado == distancia:
                                        dado_usado = valor_dado
                                        dados_disponibles.pop(i) # Remover el dado usado
                                        break
                                
                                if dado_usado is None:
                                    if selected_point == -1:
                                        mensaje_error = f"Para sacar una ficha de la barra necesitas un dado {distancia}"
                                    else:
                                        mensaje_error = f"No tienes un dado con valor {distancia}"
                                    tiempo_error = pygame.time.get_ticks()
                                    print(f"{mensaje_error}. Dados disponibles: {dados_disponibles}")
                                    selected_point = None
                                    continue
                                
                                # Intentar el movimiento con validación de dado
                                game.mover_ficha(selected_point, idx, dado_usado)
                                movimientos_realizados += 1
                                origen_str = "BARRA" if selected_point == -1 else str(selected_point + 1)
                                destino_str = "BARRA" if idx == -1 else str(idx + 1)
                                print(f"Movimiento exitoso: {origen_str} -> {destino_str} usando dado {dado_usado} ({movimientos_realizados}/{movimientos_requeridos})")
                                
                                # Verificar si hay un ganador después del movimiento
                                if game.juego_terminado():
                                    ganador = game.get_ganador()
                                    tipo_victoria = game.get_tipo_victoria()
                                    puntos = game.get_puntos_victoria()
                                    color_ganador = ganador.get_color()
                                    
                                    mensaje_victoria = f"¡Felicitaciones ganador ({color_ganador})!"
                                    
                                    print(f"\n🏆 {mensaje_victoria}")
                                    print("¡Juego terminado!")
                                
                                # Verificar si se han usado todos los dados
                                # Solo cambiar turno si el juego NO ha terminado
                                if movimientos_realizados >= movimientos_requeridos and not game.juego_terminado():
                                    print("¡Turno completado! Cambiando turno...")
                                    game.cambiar_turno()
                                    dados_tirados = False
                                    movimientos_realizados = 0
                                    movimientos_requeridos = 0
                                    dados_disponibles = []
                                    print(f"Turno de: {game.get_turno_actual().get_name()}")
                                elif movimientos_realizados >= movimientos_requeridos and game.juego_terminado():
                                    # Si terminó el juego, detener la actualización
                                    dados_tirados = False
                                    movimientos_realizados = 0
                                    movimientos_requeridos = 0
                                    dados_disponibles = []
                            except MovimientoInvalidoError as ex:
                                mensaje_error = str(ex)
                                tiempo_error = pygame.time.get_ticks()
                                print(f"Movimiento inválido: {ex}")
                            except JuegoTerminadoError as ex:
                                print(f"Juego terminado: {ex}")
                                running = False # Terminar el juego si ya hay un ganador
                            except Exception as ex:
                                mensaje_error = f"Error inesperado: {ex}"
                                tiempo_error = pygame.time.get_ticks()
                                print(mensaje_error)
                            finally:
                                selected_point = None

        # Render + actualizar hitmap
        hitmap = render_board(screen, game, font, selected_point)

        # Dibujar información del juego
        info_text = f"Turno: {game.get_turno_actual().get_name()}"
        if dados_tirados:
            info_text += f" | Dados: {game.get_dice().get_valores()} | Movimientos: {movimientos_realizados}/{movimientos_requeridos}"
        else:
            info_text += " | Presiona ESPACIO para tirar dados"
        
        text_surface = font.render(info_text, True, TEXT)
        screen.blit(text_surface, (10, 10))
        
        # Dibujar botón "Pasar" si hay dados tirados
        if dados_tirados:
            button_width = 120
            button_height = 40
            button_x = WIDTH - SAVED_AREA_WIDTH - button_width - 30  # Evitar superposición con área guardada
            button_y = 10
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Color del botón (naranja)
            button_color = (255, 165, 0)
            pygame.draw.rect(screen, button_color, button_rect, border_radius=8)
            pygame.draw.rect(screen, (200, 100, 0), button_rect, 2, border_radius=8)
            
            # Texto del botón
            button_font = pygame.font.SysFont(None, 28, bold=True)
            button_text = button_font.render("PASAR", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, button_text_rect)
        
        # Dibujar mensaje de error si existe y no ha expirado
        if mensaje_error and tiempo_error:
            # El mensaje dura 3 segundos
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_error < 3000:
                # Usar fuente más grande para el error
                error_font = pygame.font.SysFont(None, 32, bold=True)
                error_surface = error_font.render(mensaje_error, True, (200, 50, 50))
                # Centrar el mensaje en la parte inferior
                error_rect = error_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
                # Fondo semitransparente
                bg_rect = pygame.Rect(error_rect.left - 10, error_rect.top - 5, 
                                      error_rect.width + 20, error_rect.height + 10)
                pygame.draw.rect(screen, (255, 255, 200), bg_rect)
                pygame.draw.rect(screen, (200, 50, 50), bg_rect, 2)
                screen.blit(error_surface, error_rect)
            else:
                mensaje_error = None
                tiempo_error = 0
        
        # Dibujar mensaje de victoria persistente
        if mensaje_victoria and game.juego_terminado():
            # Usar fuente grande y llamativa para la victoria
            victoria_font = pygame.font.SysFont(None, 48, bold=True)
            victoria_surface = victoria_font.render(mensaje_victoria, True, (255, 215, 0))
            # Centrar el mensaje en el centro de la pantalla
            victoria_rect = victoria_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            # Fondo destacado
            bg_victoria = pygame.Rect(victoria_rect.left - 30, victoria_rect.top - 20, 
                                      victoria_rect.width + 60, victoria_rect.height + 40)
            # Dibujar sombra
            shadow_rect = pygame.Rect(bg_victoria.x + 5, bg_victoria.y + 5, bg_victoria.width, bg_victoria.height)
            pygame.draw.rect(screen, (0, 0, 0, 150), shadow_rect, border_radius=15)
            # Dibujar fondo principal
            pygame.draw.rect(screen, (255, 255, 255), bg_victoria, border_radius=15)
            pygame.draw.rect(screen, (255, 215, 0), bg_victoria, 4, border_radius=15)
            screen.blit(victoria_surface, victoria_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()