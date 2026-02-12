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
    
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30


    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
