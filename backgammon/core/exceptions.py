class GameError(Exception):
    """Excepción base para errores del juego"""
    pass


class MovimientoInvalidoError(GameError):
    """Excepción para movimientos inválidos"""
    pass


class JuegoTerminadoError(GameError):
    """Excepción para operaciones en un juego terminado"""
    pass