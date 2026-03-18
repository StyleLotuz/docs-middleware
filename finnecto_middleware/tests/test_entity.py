from modules.invoice.domain.entities.invoice_item import InvoiceItem
from modules.invoice.domain.entities.invoice import Invoice

def _build_invoice() -> Invoice:
    items = [
        InvoiceItem("Item 1", 30000, 390000, "VISTA"),
        InvoiceItem("Item 2", 30000, 390000, "CORRIENTE"),
    ]
    
    return Invoice("FNCT0006", "2026-03-03", "2026-03-20", "COP", 780000, items)

def test_apply_tax_update_item_totals():
    invoice = _build_invoice()
    invoice.apply_tax(0.19)
    
    assert invoice.items[0].total == 464100
    assert invoice.items[1].total == 464100
    
def test_apply_tax_does_not_modify_unit_price():
    invoice = _build_invoice()
    invoice.apply_tax(0.19)
    
    assert invoice.items[0].unit_price == 30000
    assert invoice.items[0].unit_price == 30000
    
def test_apply_tax_recalculates_total():
    invoice = _build_invoice()
    invoice.apply_tax(0.19)
    
    assert invoice.total == 928200
    
def test_calculate_total_sums_items():
    invoice = _build_invoice()
    invoice.items[0].total = 100000
    invoice.items[1].total = 200000
    invoice.calculate_total()
    
    assert invoice.total == 300000
    
