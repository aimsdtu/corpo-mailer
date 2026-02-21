"""Per-request Database dependency for FastAPI."""
from __future__ import annotations

from typing import AsyncGenerator

from app.db.database import Database
from app.db.engine import get_engine


async def get_db() -> AsyncGenerator[Database, None]:
    """Yield a Database wrapping a transactional connection.

    Auto-commits on clean exit, rolls back on exception.
    """
    async with get_engine().begin() as conn:
        yield Database(conn)