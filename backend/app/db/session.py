"""Database session management"""
import os
from typing import AsyncGenerator
from app.db.protocol import Database
from app.db.supabase import SupabaseDatabase
from app.core.config import get_settings
from functools import lru_cache

settings = get_settings()

@lru_cache()
async def get_database() -> Database:
    """Initialize and return the database instance"""
    return SupabaseDatabase(connection_string=settings.supabase_url)