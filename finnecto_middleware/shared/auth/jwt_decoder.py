import jwt
from jwt.exceptions import JWTDecodeError
from config import settings
from shared.auth.jwt_claims import JWTClaims

def extract_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise JWTDecodeError("Missing or invalid Authorization header")
    return authorization.removeprefix("Bearer ")

def decode_jwt(token: str) -> JWTClaims:
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_decode_secret,
            algorithms=["HS256"],
        )
    except JWTDecodeError:
        raise
    
    return JWTClaims(**payload)