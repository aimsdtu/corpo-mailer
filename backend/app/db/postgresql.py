from app.db.protocol import Database
from typing import Any, Iterable

class PostgreSQLDatabase(Database):
    def __init__(self) -> None:
        raise NotImplementedError

    def disconnect(self) -> None:
        raise NotImplementedError

    def execute(self, query: str, params: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError

    def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        raise NotImplementedError
