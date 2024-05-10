from typing import Any, Collection
from flask import request

from src.core.storage.base import Storage

class CookieStorage(Storage):
    def write(self, to: str, value: Any, **params: Any) -> None:
        resp = params['response']
        resp.set_cookie(to, value)
        
    def read(self, source: str, **params: Any) -> Any:
        return request.cookies.get(source)
    
    def read_many(self, sources: Collection[str], **params: Any) -> Any:
        return super().read_many(sources, **params)
    
    def delete(self, where: str, **params: Any) -> None:
        resp = params['response']
        resp.delete_cookie(where)

    def flush(self, **params: Any) -> None:
        resp = params['response']
        for cookie in request.cookies:
            resp.delete_cookie(cookie)