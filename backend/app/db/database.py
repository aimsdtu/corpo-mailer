"""Thin Database wrapper around an SQLAlchemy AsyncConnection.

Returns plain dicts so services stay simple.
"""
from __future__ import annotations

from typing import Any

from sqlalchemy.ext.asyncio import AsyncConnection


class Database:
    """Per-request database handle."""

    __slots__ = ("_conn",)

    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def fetch_one(self, stmt, params=None) -> dict[str, Any] | None:
        result = await self._conn.execute(stmt, params)
        row = result.mappings().first()
        return dict(row) if row else None

    async def fetch_all(self, stmt, params=None) -> list[dict[str, Any]]:
        result = await self._conn.execute(stmt, params)
        return [dict(r) for r in result.mappings().all()]

    async def execute(self, stmt, params=None) -> None:
        await self._conn.execute(stmt, params)
