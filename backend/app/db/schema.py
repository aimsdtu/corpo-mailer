"""Schema initialisation — SQLAlchemy metadata approach.

Uses SQLAlchemy's ``metadata.create_all`` via the async engine to ensure
all tables and indexes defined in ``app.db.tables`` exist. Safe to call
on every startup — SQLAlchemy emits ``CREATE TABLE IF NOT EXISTS`` /
``CREATE INDEX IF NOT EXISTS`` under the hood.
"""
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine

from app.db.tables import metadata
from app.core.logging import logger


async def ensure_schema(engine: AsyncEngine) -> None:
    """Ensure all tables and indexes from metadata exist in the database."""

    logger.info("Checking database schema…")
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    logger.info("Schema check complete")
