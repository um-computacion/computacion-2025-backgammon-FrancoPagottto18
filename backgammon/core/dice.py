import random


class Dice:
    """
    Clase que maneja la lógica de los dados en Backgammon
    """
    
    def __init__(self):
        """
        Inicializa los dados
        """
        self.__dado1__ = 0
        self.__dado2__ = 0
        self.__dados_usados__ = []
    
    def tirar(self):
        """
        Tira los dados y retorna los valores
        
        Returns:
            list: Lista con los valores de los dados [dado1, dado2]
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        self.__dados_usados__ = []
        return [self.__dado1__, self.__dado2__]
    
    def get_dados(self):
        """
        Retorna los valores actuales de los dados
        
        Returns:
            list: Lista con los valores de los dados [dado1, dado2]
        """
        return [self.__dado1__, self.__dado2__]
    
    def usar_dado(self, valor):
        """
        Marca un dado como usado
        
        Args:
            valor (int): Valor del dado a marcar como usado
            
        Raises:
            ValueError: Si el valor no está disponible
        """
        if valor not in [self.__dado1__, self.__dado2__]:
            raise ValueError(f"El valor {valor} no está disponible en los dados")
        
        if valor in self.__dados_usados__:
            raise ValueError(f"El dado con valor {valor} ya fue usado")
        
        self.__dados_usados__.append(valor)
    
    def get_dados_disponibles(self):
        """
        Retorna los valores de los dados que aún no han sido usados
        
        Returns:
            list: Lista con los valores de los dados disponibles
        """
        disponibles = []
        if self.__dado1__ not in self.__dados_usados__:
            disponibles.append(self.__dado1__)
        if self.__dado2__ not in self.__dados_usados__:
            disponibles.append(self.__dado2__)
        return disponibles
    
    def todos_dados_usados(self):
        """
        Verifica si todos los dados han sido usados
        
        Returns:
            bool: True si todos los dados han sido usados
        """
        return len(self.__dados_usados__) == 2
    
    def reset_dados_usados(self):
        """
        Resetea la lista de dados usados
        """
        self.__dados_usados__ = []
