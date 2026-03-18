import base64
import jwt
from modules.invoice.domain.strategies.basic_auth_strategy import BasicAuthStrategy
from modules.invoice.domain.strategies.jwt_auth_strategy import JWTAuthStrategy

def test_basic_auth_generates_correct_header():
    strategy = BasicAuthStrategy("legacy_user", "legacy_pass")
    header = strategy.build_auth_header()
    
    assert header.startswith("Basic ")
    encoded = header.removeprefix("Basic ")
    decoded = base64.b64decode(encoded).decode()
    assert decoded == "legacy_user:legacy_pass"

def test_jwt_auth_generates_valid_token():
    strategy = JWTAuthStrategy("mock-jwt-secret")
    header = strategy.build_auth_header()
    
    assert header.startswith("Bearer ")
    token = header.removeprefix("Bearer ")
    payload = jwt.decode(token, "mock-jwt-secret", algorithms=["HS256"], audience="taxeable-api")
    assert payload["iss"] == "middleware-mock"
    assert payload["aud"] == "taxeable-api"
    assert "exp" in payload
    