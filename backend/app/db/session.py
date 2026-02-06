from typing import AsyncGenerator
from app.db.protocol import Database
from app.db.postgresql import PostgreSQLDatabase

async def get_db_session() -> AsyncGenerator[Database, None]:
    db = PostgreSQLDatabase()
    # Logic for connecting/disconnecting would go here
    yield db

