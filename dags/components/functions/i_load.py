from abc import ABC, abstractmethod

class ILoader(ABC):
    
    @abstractmethod
    def load(self) -> None:
        """Carga los datos en la base de datos"""
        pass