import json
from typing import Type, TypeVar, Generic

from core.storage.cache_storage import CacheStorage
from core.storage.base import Storage

from core.client.base import User
from dataclasses import asdict

UserClassT = TypeVar("UserClassT", bound=User)

class InvalidUserException(Exception):
    pass

# TODO: repository to handle reading/writing users from/to storage
class UserRepository(Generic[UserClassT]):
    _storage_cls: Type[Storage]

    def __init__(self, user_cls: Type[UserClassT]) -> None:
        self._storage = self._storage_cls()
        self._user_cls = user_cls

    def _get_user_object(self, raw_user: str) -> UserClassT:
        try:
            user_dict = json.loads(raw_user)
        except json.JSONDecodeError:
            raise InvalidUserException(
                f'Error when parsing user, not valid JSON: \n{raw_user}')
        user = self._user_cls(**user_dict)
        return user

    def get_user(self, user_email: str) -> UserClassT | None:
        user_raw = self._storage.read(f"user:{user_email}")

        if not user_raw:
            return None
        
        user = self._get_user_object(user_raw)
        return user

    def save_user(self, user: UserClassT) -> None:
        self._storage.write(f'user:{user.email}', json.dumps(asdict(user)))

UserRepository._storage_cls = CacheStorage