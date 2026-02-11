"""Database protocol definition"""
from typing import Protocol, Any, Optional


class Database(Protocol):
    """Protocol defining database interface"""
    
    async def connect(self) -> None:
        """Establish database connection"""
        ...
    
    async def disconnect(self) -> None:
        """Close database connection"""
        ...
    
    async def fetch_one(self, query: str, params: Optional[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
        """Fetch a single row"""
        ...
    
    async def fetch_all(self, query: str, params: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Fetch all rows"""
        ...
    
    async def execute(self, query: str, params: Optional[dict[str, Any]] = None) -> None:
        """Execute a query without returning results"""
        ...