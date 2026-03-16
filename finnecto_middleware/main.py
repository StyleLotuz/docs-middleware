from fastapi import FastAPI
from modules.invoice.presentation.controllers.invoice_controller import router as invoice_router
from fastapi.exceptions import RequestValidationError
from jwt.exceptions import JWTDecodeError
import httpx

from shared.exceptions.handlers import (
    jwt_exception_handler,
    validation_exception_handler,
    http_forward_exception_handler,
    connect_exception_handler,
    timeout_exception_handler
)

app = FastAPI(
    title="Finnecto Middleware",
    description="Integration middleware for multi-system invoice processing",
    version="0.1.0"
)

app.add_exception_handler(JWTDecodeError, jwt_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(httpx.HTTPStatusError, http_forward_exception_handler)
app.add_exception_handler(httpx.ConnectError, connect_exception_handler)
app.add_exception_handler(httpx.TimeoutException, timeout_exception_handler)    

app.include_router(invoice_router)

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "finnecto_middleware"}