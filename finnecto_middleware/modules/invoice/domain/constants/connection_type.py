from enum import Enum

class ConnectionType(str, Enum):
    LEGACY = "legacy"
    TAXEABLE = "taxeable"