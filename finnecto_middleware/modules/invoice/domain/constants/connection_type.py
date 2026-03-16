from enum import Enum

class ConnectionType(Enum, str):
    LEGACY = "legacy"
    TAXEABLE = "taxeable"