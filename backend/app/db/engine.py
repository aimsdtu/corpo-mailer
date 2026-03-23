"""Async SQLAlchemy engine — singleton lifecycle."""
from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings
from app.core.logging import logger
from app.db.tables import metadata

_engine: AsyncEngine | None = None

def _make_url(dsn: str) -> str:
    """Convert a standard postgres DSN to the asyncpg driver URL."""
    if dsn.startswith("postgresql://"):
        return dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
    if dsn.startswith("postgres://"):
        return dsn.replace("postgres://", "postgresql+asyncpg://", 1)
    return dsn


async def init_db() -> None:
    global _engine
    settings = get_settings()
    _engine = create_async_engine(
        _make_url(settings.supabase_url),
        pool_size=3,
        max_overflow=0,
        connect_args={"ssl": "require", "statement_cache_size": 0},
    )
    async with _engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    logger.info("Database initialised")


async def close_db() -> None:
    global _engine
    if _engine:
        await _engine.dispose()
        _engine = None
        logger.info("Database disposed")


def get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("Database not initialised")
    return _engine
