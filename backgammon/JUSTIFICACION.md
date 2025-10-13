# Justificación del Proyecto Backgammon

## Resumen del Diseño General

El proyecto implementa un juego de Backgammon en Python con arquitectura de separación entre lógica de negocio y presentación. La estructura modular permite mantener el core del juego independiente de las interfaces de usuario

**Arquitectura:**
- **Core**: Lógica central (Game, Board, Player, Dice, Checker)
- **CLI**: Interfaz de línea de comandos
- **Pygame UI**: Interfaz gráfica
- **Tests**: Cobertura del 90%

## Justificación de las Clases Elegidas

- **Game**: Coordina el flujo del juego y gestiona el estado global. Centraliza turnos, validaciones y control del flujo
- **Board**: Representa el tablero de 24 puntos y gestiona posiciones de fichas. Encapsula la lógica del tablero
- **Player**: Representa un jugador (nombre, color). Modela la entidad de forma simple
- **Dice**: Gestiona tiradas de dados y valida tiradas dobles. Encapsula lógica de dados
- **Checker**: Representa una ficha individual con su color. Modela entidades básicas del juego

## Justificación de Atributos

Todos los atributos usan `__atributo__` según los requisitos del proyecto:
- **Game**: `__tablero__`, `__jugadores__`, `__dados__`, `__turno_actual__`
- **Board**: `__puntos__`, `__barra_blanca__`, `__barra_negra__`
- **Player**: `__nombre__`, `__color__`
- **Dice**: `__dado1__`, `__dado2__`, `__ultima_tirada__`

## Decisiones de Diseño Relevantes

- **Separación Core/UI**: Permite reutilización, facilita testing y mantenimiento
- **Listas para tablero**: Fácil manipulación de fichas y representación natural de pilas
- **Validaciones en Game**: Lógica centralizada y consistencia en reglas del juego
- **CLI obligatoria**: Accesibilidad y facilita testing automatizado

## Excepciones y Manejo de Errores

**Excepciones definidas:**
- **MovimientoInvalidoException**: Movimientos que violan reglas del juego
- **PosicionInvalidaException**: Posiciones fuera del tablero
- **JugadorInvalidoException**: Operaciones con jugadores inexistentes

**Estrategia:** Validación temprana, mensajes descriptivos y recuperación controlada

## Estrategias de Testing y Cobertura

**Cobertura objetivo:** 90%

**Tipos de tests:**
- Tests unitarios para cada clase del core
- Tests de integración para flujos completos
- Tests de validación de reglas de negocio
- Tests de manejo de excepciones

**Qué se prueba:** Constructores, métodos públicos, casos límite, validaciones y excepciones

## Principios SOLID y su Cumplimiento

- **SRP**: Cada clase tiene una sola responsabilidad (Game coordina, Board maneja tablero, etc.)
- **OCP**: Interfaces CLI/Pygame permiten extensión sin modificar core
- **LSP**: Implementaciones de UI son intercambiables
- **ISP**: Interfaces específicas para cada responsabilidad
- **DIP**: Game depende de abstracciones, no implementaciones concretas

## Anexos

### Diagrama de Clases
```
Game
├── Board (composición)
├── Player[] (agregación)  
├── Dice (composición)
└── UI Interface (dependencia)
```

### Flujo de Ejecución
1. Inicialización del juego
2. Configuración del tablero
3. Creación de jugadores
4. Bucle principal: tirar dados → mostrar estado → solicitar movimiento → validar → ejecutar → verificar victoria
5. Finalización y resultado

Esta arquitectura garantiza mantenibilidad, testabilidad y extensibilidad del código
