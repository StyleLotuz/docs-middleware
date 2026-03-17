from shared.auth.jwt_claims import JWTClaims
from modules.invoice.domain.constants.connection_type import ConnectionType
from modules.invoice.domain.interfaces.invoice_transformer import IInvoiceTransformer
from modules.invoice.domain.interfaces.auth_strategy import IAuthStrategy
from modules.invoice.domain.transformers.legacy_transformer import LegacyTransformer
from modules.invoice.domain.transformers.taxeable_transformer import TaxeableTransformer
from modules.invoice.domain.strategies.basic_auth_strategy import BasicAuthStrategy
from modules.invoice.domain.strategies.jwt_auth_strategy import JWTAuthStrategy

class ConnectionFactory:
    
    @staticmethod
    def create(claims: JWTClaims) -> tuple[IInvoiceTransformer, IAuthStrategy]:
        if claims.connection_type == ConnectionType.LEGACY:
            return (
                LegacyTransformer(),
                BasicAuthStrategy(claims.username, claims.password)
            )
            
        if claims.connection_type == ConnectionType.TAXEABLE:
            if not claims.secret:
                raise ValueError("Missing secret for taxeable connection")
            return (
                TaxeableTransformer(),
                JWTAuthStrategy(claims.secret)
            )
        
        raise ValueError(f"Unsupported connection type: {claims.connection_type}")