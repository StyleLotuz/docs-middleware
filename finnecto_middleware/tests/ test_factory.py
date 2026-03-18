import pytest
from shared.auth.jwt_claims import JWTClaims
from modules.invoice.domain.factories.connection_factory import ConnectionFactory
from modules.invoice.domain.transformers.legacy_transformer import LegacyTransformer
from modules.invoice.domain.transformers.taxeable_transformer import TaxeableTransformer
from modules.invoice.domain.strategies.basic_auth_strategy import BasicAuthStrategy
from modules.invoice.domain.strategies.jwt_auth_strategy import JWTAuthStrategy

def test_factory_creates_legacy_strategies():
    claims = JWTClaims(
        connection_type="legacy",
        username="user",
        password="pass"
    )
    transformer, auth = ConnectionFactory.create(claims)
    
    assert isinstance(transformer, LegacyTransformer)
    assert isinstance(auth, BasicAuthStrategy)
    
def test_factory_creates_taxeable_strategies():
    claims = JWTClaims(
        connection_type="taxeable",
        username="user",
        password="pass",
        secret="my-secret"
    )
    transformer, auth = ConnectionFactory.create(claims)
    assert isinstance(transformer, TaxeableTransformer)
    assert isinstance(auth, JWTAuthStrategy)
    
def test_factory_raises_on_missing_secret_for_taxeable():
    claims = JWTClaims(
        connection_type="taxeable",
        username="user",
        password="pass"
    )
    
    with pytest.raises(ValueError, match="Missing secret"):
        ConnectionFactory.create(claims)
        
def test_factory_raises_on_unknown_type():
    claims = JWTClaims(
        connection_type="unknown",
        username="user",
        password="pass"
    )
    
    with pytest.raises(ValueError, match="Unsupported connection type"):
        ConnectionFactory.create(claims)