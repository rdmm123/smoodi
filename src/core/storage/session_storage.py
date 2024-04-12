from typing import Any, MutableMapping
from flask import session

from core.storage.storage import Storage

class SessionStorage(Storage):
    def __init__(self, session: MutableMapping[str, Any]) -> None:
        self.session = session

    def write(self, to: str, value: Any, **params: Any) -> None:
        self.session[to] = value
    
    def read(self, source: str, **params: Any) -> Any:
        return self.session[source]
    
    def delete(self, where: str, **params: Any) -> None:
        try:
            del session[where]
        except KeyError:
            pass

    def flush(self) -> None:
        session.clear()