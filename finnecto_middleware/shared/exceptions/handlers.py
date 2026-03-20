from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from jwt.exceptions import DecodeError
import httpx
from shared.dtos.api_response import ApiResponse

async def jwt_exception_handler(request: Request, exc: DecodeError) -> JSONResponse:
    response = ApiResponse.error(status=401, message=str(exc))
    return JSONResponse(status_code=401, content=response.model_dump())

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    response = ApiResponse.error(
        status=400, 
        message="Invalid Payload",
        errors=exc.errors(),
    )
    return JSONResponse(status_code=400, content=response.model_dump())

async def http_forward_exception_handler(request: Request, exc: httpx.HTTPStatusError) -> JSONResponse:
    response = ApiResponse.error(status=502, message="Integration error with destination system")
    return JSONResponse(status_code=502, content=response.model_dump())

async def connect_exception_handler(request: Request, exc: httpx.ConnectError) -> JSONResponse:
    response = ApiResponse.error(status=502, message="Could not connect to destination system")
    return JSONResponse(status_code=502, content=response.model_dump())

async def timeout_exception_handler(request: Request, exc: httpx.TimeoutException) -> JSONResponse:
    response = ApiResponse.error(status=502, message="Destination system timed out")
    return JSONResponse(status_code=502, content=response.model_dump())