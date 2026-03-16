import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from config import settings
from shared.auth.jwt_claims import JWTClaims

def extract_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise InvalidTokenError("Missing or invalid Authorization header")
    return authorization.removeprefix("Bearer ")

def decode_jwt(token: str) -> JWTClaims:
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_decode_secret,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
    except InvalidTokenError:
        raise
    
    return JWTClaims(**payload)