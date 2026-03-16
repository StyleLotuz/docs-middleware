from typing import Any
from modules.invoice.domain.entities.invoice import Invoice
from modules.invoice.domain.interfaces.invoice_transformer import IInvoiceTransformer

class TaxeableTransformer(IInvoiceTransformer):
    def to_target_format(self, invoice: Invoice) -> dict[str, Any]:
        return {
            "document": {
                "reference": invoice.number,
                "dates": {
                    "reception": invoice.reception_date,
                    "due": invoice.due_date
                },
                "currency": invoice.currency,
                "total": invoice.total,
                "items": [{
                    "description": item.description,
                    "unitPrice": item.unit_price,
                    "amount": item.total,
                    "account": item.account
                }
                for item in invoice.items
                ]
            }
        }
    def to_standard_format(self, response: dict[str, Any]) -> dict[str, Any]:
        document = response["document"]
        return {
            "number": document["reference"],
            "reception_date": document["dates"]["reception"],
            "due_date": document["dates"]["due"],
            "currency": document["currency"],
            "total": document["total"],
            "items": [
                {
                    "description": item["description"],
                    "unit_price": item["unitPrice"],
                    "total": item["amount"],
                    "account": item["account"]
                }
                for item in document["items"]
            ]
        }
    