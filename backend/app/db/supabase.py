"""PostgreSQL database implementation"""
import asyncpg
import re
from typing import Any, Optional
from app.db.protocol import Database


def convert_named_to_positional(query: str, params: dict[str, Any]) -> tuple[str, list[Any]]:
    """
    Convert named parameters (:name) to positional ($1, $2, etc.)
    """
    if not params:
        return query, []
    
    positional_query = query
    positional_params = []
    
    # Sort keys by length (longest first) to avoid partial replacements
    sorted_keys = sorted(params.keys(), key=len, reverse=True)
    
    for i, key in enumerate(sorted_keys, start=1):
        # Use word boundary to match exact parameter names
        pattern = r':' + re.escape(key) + r'\b'
        positional_query = re.sub(pattern, f'${i}', positional_query)
        positional_params.append(params[key])
    
    return positional_query, positional_params


class SupabaseDatabase(Database):
    """PostgreSQL database implementation using asyncpg"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: Optional[asyncpg.Pool] = None
        self._migrations_run = False 
    
    async def connect(self) -> None:
        """Create connection pool"""
        self.pool = await asyncpg.create_pool(
                    dsn=self.connection_string,
                    min_size=1,
                    max_size=3,
                    statement_cache_size=0,
                    max_inactive_connection_lifetime=60,
                    command_timeout=30,
                    timeout=30,
                    ssl="require",
        )
        print("✅ Database connected successfully")
        
        # Run migrations automatically on first connection
        if not self._migrations_run:
            await self._run_migrations()
            self._migrations_run = True
    
    async def _run_migrations(self) -> None:
        """Run database migrations"""
        try:
            from app.db.migrations import run_migrations
            await run_migrations(self)
        except Exception as e:
            print(f"⚠️  Migration error: {e}")
            # Don't raise - allow app to continue even if migrations fail
            # This way existing databases won't break
    
    async def disconnect(self) -> None:
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            print("✅ Database disconnected")
    
    async def fetch_one(self, query: str, params: Optional[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
        """Fetch a single row"""
        async with self.pool.acquire() as connection:
            if params:
                query_converted, values = convert_named_to_positional(query, params)
                row = await connection.fetchrow(query_converted, *values)
            else:
                row = await connection.fetchrow(query)
            
            return dict(row) if row else None
    
    async def fetch_all(self, query: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Fetch all rows"""
        async with self.pool.acquire() as connection:
            if params:
                query_converted, values = convert_named_to_positional(query, params)
                rows = await connection.fetch(query_converted, *values)
            else:
                rows = await connection.fetch(query)
            
            return [dict(row) for row in rows]
    
    async def execute(self, query: str, params: Optional[dict[str, Any]] = None) -> None:
        """Execute a query"""
        async with self.pool.acquire() as connection:
            if params:
                query_converted, values = convert_named_to_positional(query, params)
                await connection.execute(query_converted, *values)
            else:
                await connection.execute(query)