class InvoiceItem:
    def __init__(self, description: str, unit_price: float, total: float, account: str):
        self.description = description
        self.unit_price = unit_price
        self.total = total
        self.account = account
        
    def apply_tax(self, rate: float) -> None:
        self.total = round(self.total * (1 + rate))
        