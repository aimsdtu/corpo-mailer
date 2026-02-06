from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    project_name: str = "CorpoMailer"
    api_str: str = "/api/v1"
    secret_key: str
    database_url: str
    
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
