from fastapi import APIRouter, Header
from shared.auth.jwt_decoder import extract_token, decode_jwt
from shared.dtos.api_response import ApiResponse
from modules.invoice.presentation.dtos.invoice_input_dto import InvoiceInputDTO
from modules.invoice.application.dtos.invoice_dto import InvoiceDTO, InvoiceItemDTO
from modules.invoice.application.use_cases.invoice_forward_use_case import InvoiceForwardUseCase

router = APIRouter()

@router.post("/invoice/forward")
async def forward_invoice(
    body: InvoiceInputDTO,
    authorization: str | None = Header(default=None)
):
    token = extract_token(authorization)
    claims = decode_jwt(token)
    
    invoice_dto = InvoiceDTO(
        number=body.number,
        reception_date=body.reception_date,
        due_date=body.due_date,
        currency=body.currency,
        total=body.total,
        items=[
            InvoiceItemDTO(
                description=item.description,
                unit_price=item.unit_price,
                total=item.total,
                account=item.account
            )
            for item in body.items
        ],
    )
    
    use_case = InvoiceForwardUseCase()
    result = await use_case.execute(claims, invoice_dto)
    
    return ApiResponse.success(item=result, message="success invoice forward")