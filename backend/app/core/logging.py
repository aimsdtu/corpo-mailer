import logging
from app.core.config import get_settings
from functools import lru_cache

def setup_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format=settings.log_format
    )

@lru_cache
def get_logger(name: str = "corpo-mailer") -> logging.Logger:
    return logging.getLogger(name)

logger = get_logger()
