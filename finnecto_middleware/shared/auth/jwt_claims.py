from pydantic import BaseModel

class JWTClaims(BaseModel):
    connection_type: str
    username: str
    password: str
    secret: str | None = None
