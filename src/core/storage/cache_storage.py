import redis
from typing import Any, Collection

from src.core.storage.base import Storage
from src.core.helpers import LoadFromEnvMixin


class CacheStorage(Storage, LoadFromEnvMixin):
    host: str = ""
    port: str = ""
    username: str = ""
    password: str = ""

    load_from_env: dict[str, str] = {
        "host": "CACHE_HOST",
        "port": "CACHE_PORT",
        "username": "CACHE_USER",
        "password": "CACHE_PASS",
    }

    def __init__(self) -> None:
        self._load_attrs_from_env()
        self.cache_client = redis.Redis(
            self.host, int(self.port), username=self.username, password=self.password
        )

    def write(self, to: str, value: Any, **params: Any) -> None:
        expiry_seconds: int | None = params.get("expiry_seconds")

        self.cache_client.set(to, value, ex=expiry_seconds)

    def read(self, source: str, **params: Any) -> Any:
        return self.cache_client.get(source)

    def read_many(self, sources: Collection[str], **params: Any) -> Any:
        return self.cache_client.mget(sources)

    def delete(self, where: str, **params: Any) -> None:
        self.cache_client.delete(where)

    def flush(self, **params: Any) -> None:
        self.cache_client.flushall()
