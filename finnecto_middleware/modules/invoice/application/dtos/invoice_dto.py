from dataclasses import dataclass

@dataclass
class InvoiceItemDTO:
    description: str
    unit_price: float
    total: float
    account: str
    
@dataclass
class InvoiceDTO:
    number: str
    reception_date: str
    due_date: str
    currency: str
    total: float
    items: list[InvoiceItemDTO]