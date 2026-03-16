from fastapi import FastAPI
from modules.invoice.presentation.controllers.invoice_controller import router as invoice_router

app = FastAPI(
    title="Finnecto Middleware",
    description="Integration middleware for multi-system invoice processing",
    version="0.1.0"
)

app.include_router(invoice_router)

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "finnecto_middleware"}