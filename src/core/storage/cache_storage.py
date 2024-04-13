import redis
from typing import Any
from flask import session

from core.storage.base import Storage
from core.helpers import LoadFromEnvMixin

class CacheStorage(Storage, LoadFromEnvMixin):
    host: str = ''
    port: str = ''

    load_from_env: dict[str, str] = {
        'host': 'CACHE_HOST',
        'port': 'CACHE_PORT'
    }

    def __init__(self) -> None:
        self._load_attrs_from_env()
        self.cache_client = redis.Redis(self.host, int(self.port))

    def write(self, to: str, value: Any, **params: Any) -> None:
        self.cache_client.set(to, value)
    
    def read(self, source: str, **params: Any) -> Any:
        return self.cache_client.get(source)
    
    def delete(self, where: str, **params: Any) -> None:
        self.cache_client.delete(where)
        
    def flush(self, **params: Any) -> None:
        self.cache_client.flushall()