from pydantic import BaseModel

class InvoiceItemInputDTO(BaseModel):
    description: str
    unit_price: float
    total: float
    account: str

class InvoiceInputDTO(BaseModel):
    number: str
    reception_date: str
    due_date: str
    currency: str
    total: float
    items: list[InvoiceItemInputDTO]