from modules.invoice.domain.entities.invoice_item import InvoiceItem
from modules.invoice.domain.entities.invoice import Invoice
from modules.invoice.domain.transformers.legacy_transformer import LegacyTransformer
from modules.invoice.domain.transformers.taxeable_transformer import TaxeableTransformer

def _build_invoice() -> Invoice:
    items = [
        InvoiceItem("Item 1", 30000, 390000, "VISTA")
    ]
    return Invoice("FNCT0006", "2026-03-03", "2026-03-20", "COP", 390000, items)

# Legacy

def test_legacy_t0_target_format():
    transformer = LegacyTransformer()
    invoice = _build_invoice()
    result = transformer.to_target_format(invoice)
    
    assert result["invoice_number"] == "FNCT0006"
    assert result["recv_date"] == "2026-03-03"
    assert result["expiry_date"] == "2026-03-20"
    assert result["curr"] == "COP"
    assert result["gross_total"] == 390000
    assert len(result["lines"]) == 1
    assert result["lines"][0]["desc"] == "Item 1"
    assert result["lines"][0]["unit_price"] == 30000
    assert result["lines"][0]["line_total"] == 390000
    assert result["lines"][0]["acct"] == "VISTA"
    
def test_legacy_to_standard_format():
    transformer = LegacyTransformer()
    mock_response = {
        "invoice_number": "FNCT0006",
        "recv_date": "2026-03-03",
        "expiry_date": "2026-03-20",
        "curr": "COP",
        "gross_total": 464100,
        "lines": [
            {
                "id": "ID-123",
                "desc": "Item 1",
                "unit_price": 30000,
                "line_total": 464100,
                "acct": "VISTA",
            }
        ],
        "processed_at": "2026-03-17T00:00:00Z"
    }
    result = transformer.to_standard_format(mock_response)
    
    assert result["number"] == "FNCT0006"
    assert result["reception_date"] == "2026-03-03"
    assert result["due_date"] == "2026-03-20"
    assert result["currency"] == "COP"
    assert result["total"] == 464100
    assert len(result["items"]) == 1
    assert result["items"][0]["description"] == "Item 1"
    assert "id" not in result["items"][0]
    assert "processed_at" not in result
    
# Taxeable 

def test_taxeable_to_target_format():
    transformer = TaxeableTransformer()
    invoice = _build_invoice()
    result = transformer.to_target_format(invoice)
    
    assert result["document"]["reference"] == "FNCT0006"
    assert result["document"]["dates"]["reception"] == "2026-03-03"
    assert result["document"]["dates"]["due"] == "2026-03-20"
    assert result["document"]["currency"] == "COP"
    assert result["document"]["total"] == 390000
    assert len(result["document"]["items"]) == 1
    assert result["document"]["items"][0]["unitPrice"] == 30000
    assert result["document"]["items"][0]["amount"] == 390000
    
def test_taxeable_to_standard_format():
    transformer = TaxeableTransformer()
    mock_response = {
        "document": {
            "reference": "FNCT0006",
            "dates": {
                "reception": "2026-03-03",
                "due": "2026-03-20"
            },
            "currency": "COP",
            "total": 390000,
            "items": [
                {
                    "id": "ID-456",
                    "description": "Item 1",
                    "unitPrice": 30000,
                    "amount": 390000,
                    "account": "VISTA"
                }
            ],
            "processedAt": "2026-03-17T00:00:00Z",
        }
    }
    result = transformer.to_standard_format(mock_response)
    
    assert result["number"] == "FNCT0006"
    assert result["reception_date"] == "2026-03-03"
    assert result["total"] == 390000
    assert result["items"][0]["unit_price"] == 30000
    assert result["items"][0]["total"] == 390000
    assert "id" not in result["items"][0]
    