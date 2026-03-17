import logging

import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError

from config import settings
from shared.auth.jwt_claims import JWTClaims

logger = logging.getLogger(__name__)

def extract_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise DecodeError("Missing or invalid Authorization header")

    return authorization.removeprefix("Bearer ")

def decode_jwt(token: str) -> JWTClaims:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_decode_secret,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        raise DecodeError("Token has expired")
    except DecodeError:
        raise
    
    claims = JWTClaims(**payload)
    logger.info("JWT decoded | connection_type=%s | username=%s", claims.connection_type, claims.username)
    
    return claims
    
