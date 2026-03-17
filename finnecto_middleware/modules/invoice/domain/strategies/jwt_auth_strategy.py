from datetime import datetime, timedelta, UTC
import jwt
from modules.invoice.domain.interfaces.auth_strategy import IAuthStrategy

class JWTAuthStrategy(IAuthStrategy):
    
    def __init__(self, secret: str):
        self.secret = secret
        
    def build_auth_header(self) -> str:
        payload = {
            "iss": "middleware-mock",
            "aud": "taxeable-api",
            "exp": datetime.now(UTC) + timedelta(hours=1)
        }
        token = jwt.encode(payload, self.secret, algorithm="HS256")
        return f"Bearer {token}"