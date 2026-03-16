from typing import Any
from pydantic import BaseModel

class ApiResponse(BaseModel):
    status: int
    message: str
    item: Any | None = None
    errors: Any | None = None

    @classmethod
    def success(cls, item: Any, message: str="success") -> "ApiResponse":
        return cls(status=200, message=message, item=item, errors=None)
    
    @classmethod
    def error(cls, status: int, message: str, errors: Any| None = None) -> "ApiResponse":
        return cls(status=status, message=message, item=None, errors=errors)    