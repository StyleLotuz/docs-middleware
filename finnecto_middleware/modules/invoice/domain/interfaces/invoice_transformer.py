from abc import ABC, abstractmethod
from typing import Any

from modules.invoice.domain.entities.invoice import Invoice

class IInvoiceTransformer(ABC):
    
    @abstractmethod
    def to_target_format(self, invoice: Invoice) -> dict[str, Any]:
        ...
        
    @abstractmethod
    def to_standard_format(self, response: dict[str, Any]) -> dict[str, Any]:
        ...