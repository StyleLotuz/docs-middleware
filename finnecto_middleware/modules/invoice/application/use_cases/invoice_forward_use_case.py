from typing import Any
from shared.auth.jwt_claims import JWTClaims
from shared.services.http_forwarder import forward_request
from modules.invoice.application.dtos.invoice_dto import InvoiceDTO
from modules.invoice.domain.constants.connection_type import ConnectionType
from modules.invoice.domain.entities.invoice import Invoice
from modules.invoice.domain.entities.invoice_item import InvoiceItem
from modules.invoice.domain.factories.connection_factory import ConnectionFactory

TAX_RATE = 0.19

class InvoiceForwardUseCase:
    async def execute(self, claims: JWTClaims, invoice_dto: InvoiceDTO) -> dict[str, Any]:
        invoice = self._build_entity(invoice_dto)
        transformer, auth_strategy = ConnectionFactory.create(claims)
        
        if claims.connection_type == ConnectionType.LEGACY:
            invoice.apply_tax(TAX_RATE)
            
        body = transformer.to_target_format(invoice)
        auth_header = auth_strategy.build_auth_header()
        
        response = await forward_request(
            connection_type=claims.connection_type,
            body=body,
            auth_header=auth_header
        )
        
        result = transformer.to_standard_format(response)
        return result
        
    def _build_entity(self, dto: InvoiceDTO) -> Invoice:
        items = [
            InvoiceItem(
                description=item.description,
                unit_price=item.unit_price,
                total=item.total,
                account=item.account,
            )
            for item in dto.items
        ]
        
        return Invoice(
            number=dto.number,
            reception_date=dto.reception_date,
            due_date=dto.due_date,
            currency=dto.currency,
            total=dto.total,
            items=items
        )