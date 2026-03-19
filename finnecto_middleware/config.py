from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Modo estricto: estas variables deben existir en `.env` o por env vars.
    mock_server_url: str
    jwt_decode_secret: str
    
    model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parent / ".env"))
    
settings = Settings()