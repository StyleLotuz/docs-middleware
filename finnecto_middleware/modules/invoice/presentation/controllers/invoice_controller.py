from fastapi import APIRouter

router = APIRouter()

@router.post("/invoice/forward")
async def forward_invoice():
    return {"status": "not implemented"}