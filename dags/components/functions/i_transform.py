from typing import Any
from abc import ABC, abstractmethod

class IBaseDataTransformer(ABC):
    """Interfaz base para transformadores de datos"""
    
    @abstractmethod
    def transform(self, **kwargs) -> Any:
        """Método principal de transformación"""
        pass