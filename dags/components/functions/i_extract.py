from abc import ABC, abstractmethod

class IExtractData(ABC):

    @abstractmethod
    def get_api_bash_command(self) -> str:
        """Devolver el comando Bash para extraer datos"""
        pass

    @abstractmethod
    def get_api_python(self) -> None:
        """Extraer datos desde la API usando Python"""
        pass