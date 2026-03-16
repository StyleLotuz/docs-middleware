from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Usamos valores por defecto en nuestras variables para hacer mas facil levantarlas
    # En un caso de produccion seria mas eficiente no dar este valor y 
    # En ese caso la variables tendria que estar si o si en el .env
    mock_server_url: str = "http://localhost:3000"
    jwt_decode_secret: str = "incoming-jwt-dev-secret"
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()