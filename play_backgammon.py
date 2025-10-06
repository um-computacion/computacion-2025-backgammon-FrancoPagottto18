#!/usr/bin/env python3
"""
Script ejecutable para jugar Backgammon
Permite ejecutar el juego directamente desde la línea de comandos
"""

import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
# Esto permite importar módulos de 'backgammon.cli'
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backgammon.cli.main import main

if __name__ == "__main__":
    main()
