from typing import Any
from modules.invoice.domain.entities.invoice import Invoice
from modules.invoice.domain.interfaces.invoice_transformer import IInvoiceTransformer

class LegacyTransformer(IInvoiceTransformer):
    def to_target_format(self, invoice: Invoice) -> dict[str, Any]:
        return {
            "invoice_number": invoice.number,
            "recv_date": invoice.reception_date,
            "expiry_date": invoice.due_date,
            "curr": invoice.currency,
            "gross_total": invoice.total,
            "lines": [
                {
                    "desc": item.description,
                    "unit_price": item.unit_price,
                    "line_total": item.total,
                    "acct": item.account
                }
                for item in invoice.items
            ]
        }
    
    def to_standard_format(self, response: dict[str, Any]) -> dict[str, Any]:
        return {
            "number": response["invoice_number"],
            "reception_date": response["recv_date"],
            "due_date": response["expiry_date"],
            "currency": response["curr"],
            "total": response["gross_total"],
            "items": [
               {
                   "description": line["desc"],
                   "unit_price": line["unit_price"],
                   "total": line["line_total"],
                   "account": line["acct"]
               }
               for line in response["lines"] 
            ]            
        }
