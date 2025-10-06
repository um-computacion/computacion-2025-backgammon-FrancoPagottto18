"""
Punto de entrada para ejecutar la CLI como módulo
Permite ejecutar: python -m backgammon.cli
"""

import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from backgammon.cli.main import main

if __name__ == "__main__":
    main()
