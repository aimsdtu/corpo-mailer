from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    env: str
    project_name: str = "CorpoMailer"
    api_str: str = "/api/v1"
    secret_key: str
    supabase_url: str
    
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 10
    jwt_refresh_token_expire_days: int = 7

    # Google OAuth
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:8000/api/v1/auth/callback/google"

    # CORS
    frontend_origin: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
