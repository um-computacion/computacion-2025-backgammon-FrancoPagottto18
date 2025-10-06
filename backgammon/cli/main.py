
"""
Interfaz de línea de comandos para el juego de Backgammon
Permite a los jugadores interactuar con el juego mediante comandos de texto
"""

import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
# Esto permite importar módulos de 'backgammon.core'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backgammon.core.game import Game
from backgammon.core.exceptions import MovimientoInvalidoError, JuegoTerminadoError


