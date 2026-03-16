from abc import ABC, abstractmethod

class IAuthStrategy(ABC):
    
    @abstractmethod
    def build_auth_header(self) -> str:
        ...