import base64

from modules.invoice.domain.interfaces.auth_strategy import IAuthStrategy

class BasicAuthStrategy(IAuthStrategy):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        
    def build_auth_header(self) -> str:
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"