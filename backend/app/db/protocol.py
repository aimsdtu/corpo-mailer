from typing import Protocol, Any, Iterable

class Database(Protocol):
    def disconnect(self) -> None:
        raise NotImplementedError

    def execute(self, query: str, params: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError

    def fetch_all(self, query: str, params: dict[str, Any] | None = None) -> Iterable[dict[str, Any]]:
        raise NotImplementedError

    def fetch_one(self, query: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        raise NotImplementedError
