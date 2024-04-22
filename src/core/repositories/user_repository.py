import json
from typing import Type, TypeVar, Generic
from flask import current_app
from collections.abc import Collection

from core.storage.cache_storage import CacheStorage
from core.storage.base import Storage

from core.client.base import User
from dataclasses import asdict

UserClassT = TypeVar("UserClassT", bound=User)

class InvalidJsonException(Exception):
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
            raise InvalidJsonException(
                f'Error when parsing user, not valid JSON: \n{raw_user}')
        user = self._user_cls(**user_dict)
        return user

    def get_user(self, user_id: str) -> UserClassT | None:
        user_raw = self._storage.read(f"user:{user_id}")

        if not user_raw:
            return None
        
        user = self._get_user_object(user_raw)
        return user
    
    def get_user_id(self, user_email: str) -> str | None:
        user_id: bytes | None = self._storage.read(f"user:email:{user_email}")
        return user_id.decode() if user_id else None
    
    def get_user_by_email(self, user_email: str) -> tuple[str | None, UserClassT | None]:
        user_id = self.get_user_id(user_email)

        if user_id is None:
            return None, None
        
        return user_id, self.get_user(user_id)
    
    def get_users(self, user_ids: Collection[str]) -> list[UserClassT]:
        users_raw: list[str | None] = self._storage.read_many([
            f'user:{u_id}' for u_id in user_ids
        ])
        current_app.logger.debug(f'users raw {users_raw}')
        users: list[UserClassT] = []

        for user_raw in users_raw:
            if user_raw is None:
                continue
            users.append(self._get_user_object(user_raw))

        return users
    
    def get_user_session(self, user_id: str) -> list[UserClassT]:
        session_raw = self._storage.read(f"session:{user_id}")

        if not session_raw:
            return []
        
        try:
            session: list[str] = json.loads(session_raw)
        except json.JSONDecodeError:
            raise InvalidJsonException(
                f'Error when parsing session, not valid JSON: \n{session_raw}')
        
        users = self.get_users(session)
        
        return users
    
    def save_user(self, user: UserClassT) -> None:
        self._storage.write(f'user:{user.id}', json.dumps(asdict(user)))
        self._storage.write(f'user:email:{user.email}', user.id)

    def delete_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        if not user:
            return
        
        self._storage.delete(f"user:{user_id}")
        self._storage.delete(f"user:email:{user.email}")
        self._storage.delete(f"session:{user_id}")


UserRepository._storage_cls = CacheStorage