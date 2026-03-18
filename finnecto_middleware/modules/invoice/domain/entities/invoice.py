from modules.invoice.domain.entities.invoice_item import InvoiceItem

class Invoice:
    def __init__(
            self, 
            number: str, 
            reception_date: str, 
            due_date: str,
            currency: str,
            total: float,
            items: list[InvoiceItem]
        ):
        self.number = number
        self.reception_date = reception_date
        self.due_date = due_date
        self.currency = currency
        self.total = total
        self.items = items
        
    def apply_tax(self, rate: float) -> None:
        for item in self.items:
            item.apply_tax(rate)
        self.calculate_total()    
        
    def calculate_total(self) -> None:
        self.total = sum(item.total for item in self.items)