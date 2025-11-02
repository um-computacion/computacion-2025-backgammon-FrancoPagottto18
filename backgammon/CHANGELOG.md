# Changelog

Este documento sigue el formato Keep a Changelog. Los cambios se agrupan por categorías: Added, Changed y Fixed.


### Added
- 2025-11-01: Implemento área de fichas guardadas en pygame_ui con hitmap para bear off desde área dedicada
- 2025-11-01: Implemento detección automática de victoria cuando se retiran todas las fichas del tablero
- 2025-11-01: Modifico regla de bear off para permitir usar dados mayores o iguales a la distancia requerida
- 2025-11-01: Agrego tests adicionales para alcanzar 90% de cobertura en game.py y cli/main.py (bear off, gammon/backgammon, manejo de excepciones)
- 2025-10-11: Termino con la implementación de los tests de CLI
- 2025-10-10: Comienzo a implementar testeo del CLI
- 2025-10-07: Cambio la implementación del cliente y agrego validaciones de los dados en el juego
- 2025-10-06: Comienzo de implementación de interfaz para el usuario
- 2025-10-05: Comienzo con el interfaz del juego
- 2025-10-04: Finalizo con los tests de game
- 2025-10-03: Continuo con los tests de game
- 2025-10-01: Agrego get_ganador, juego_terminado, reiniciar_juego
- 2025-09-30: Implementación de la función que verifica ganador
- 2025-09-29: Continuo con la función para mover la ficha
- 2025-09-28: Continuo la implementación del juego
- 2025-09-27: Continuo con la implementación de la función para mover fichas
- 2025-09-26: Agrego función y excepciones para mover ficha
- 2025-09-24: Agrego función cambiar turnos
- 2025-09-23: Agrego más getters
- 2025-09-21: Agrego getters para el juego
- 2025-09-19: Comienzo con la implementación del juego con la función que inicializa el juego
- 2025-09-18: Agrego test para que el constructor acepte diferentes colores
- 2025-09-18: Agrego tests de get_name y get_color
- 2025-09-15: Agrego tests unitarios para la clase player
- 2025-09-14: Agrego test para la tirada doble y el de repr para representar el objeto
- 2025-09-13: Agrego test para la tirada normal de los dados
- 2025-09-12: Agrego test de estado_inicial de dice
- 2025-09-10: Agrego tests de la clase checker
- 2025-09-09: Agrego test de agregar_barra y quitar_barra
- 2025-09-08: Agrego tests para agregar y quitar fichas del punto
- 2025-09-08: Comenzando la integración continua
- 2025-09-07: Agrego primer test para inicializar tablero
- 2025-09-05: Agrego get_dado1 y dos y repr para depuración
- 2025-09-04: Agrego get_valores y es_doble si la última tirada fue doble
- 2025-09-02: Agrego información personal al README y información del proyecto al CHANGELOG
- 2025-09-01: Agrego la función tirar
- 2025-08-31: Comienzo la implementación del dado del backgammon
- 2025-08-28: Agrego función obtener_barra y obtener_punto
- 2025-08-27: Agrego manejo de barras (agregar_barra y quitar_barra)
- 2025-08-26: Agrego métodos para agregar y quitar ficha
- 2025-08-25: Agrego la clase player para representar a un jugador
- 2025-08-24: Agrego inicializar_tablero
- 2025-08-23: Agrego clase checker para representar fichas del juego
- 2025-08-22: Implementación de clase board con algunos atributos
- 2025-08-22: Termino la estructura base del proyecto
- 2025-08-21: Comienzo de estructuración de carpetas para el juego backgammon

### Changed
- 2025-11-01: Simplifico mensaje de victoria para mostrar solo el color del ganador
- 2025-11-01: Mejoro cobertura de tests: game.py alcanza 94% y cli/main.py alcanza 90%
- 2025-10-05: Modifico gitignore
- 2025-10-05: Correcciones generales en el código
- 2025-08-28: Corrección de tipeo en atributos (Player)
- 2025-08-27: Corrección de código y elimino código de checker que no pertenece a esta rama
- 2025-08-24: Elimino código
- 2025-08-22: Merge pull request #4 desde 1-estructura-de-proyecto
- 2025-08-21: Configuración de GitHub Classroom Feedback

### Fixed
- 2025-11-01: Corrección de hit_test en pygame_ui/main.py para usar hasattr en lugar de isinstance
- 2025-10-05: Corrección de error de indentación en test_tirar_dados_juego_terminado
- 2025-10-05: Corrección de errores en tests
- 2025-09-04: Corrección, agrego pop() porque con el remove no va a encontrar la instancia
- 2025-08-28: Corrección de tipeo en atributos
- 2025-08-27: Corrección de código y elimino código de checker que no pertenece a esta rama
- 2025-08-26: Corrección de error
- 2025-08-25: Corrección de error
- 2025-08-25: Corrección de error de código
- 2025-08-23: Corrección, la ficha se representa con el color
