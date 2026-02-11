"""Database session management"""
import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from app.db.postgresql import PostgreSQLDatabase
from app.db.protocol import Database

load_dotenv()

# Global database instance
_db: PostgreSQLDatabase = None


async def get_database() -> PostgreSQLDatabase:
    """Get database instance"""
    global _db
    if _db is None:
        connection_string = os.getenv("DATABASE_URL")
        print("🔥 USING DATABASE_URL:", connection_string)

        if not connection_string:
            raise ValueError("DATABASE_URL not found in environment variables")
        
        _db = PostgreSQLDatabase(connection_string)
        await _db.connect()
    
    return _db


async def get_db_session() -> AsyncGenerator[Database, None]:
    """Dependency for FastAPI routes"""
    db = await get_database()
    yield db


async def close_database():
    """Close database connection"""
    global _db
    if _db:
        await _db.disconnect()
        _db = None