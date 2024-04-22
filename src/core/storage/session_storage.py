from typing import Any, Collection
from flask import session

from core.storage.base import Storage

class SessionStorage(Storage):
    def write(self, to: str, value: Any, **params: Any) -> None:
        session[to] = value
    
    def read(self, source: str, **params: Any) -> Any:
        return session[source]
    
    def read_many(self, sources: Collection[str], **params: Any) -> Any:
        return super().read_many(sources, **params)
    
    def delete(self, where: str, **params: Any) -> None:
        try:
            del session[where]
        except KeyError:
            pass

    def flush(self, **params: Any) -> None:
        session.clear()