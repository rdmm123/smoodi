from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any, Self, ClassVar, Type

SUCCESS_STATUSES = [200]

class APIModel:
    @classmethod
    def from_api_response(cls, response: dict[str, Any]) -> Self:
        raise NotImplementedError
    
@dataclass
class Artist(APIModel):
    name: str
    url: str

@dataclass
class Track(APIModel):
    name: str
    external_url: str
    uri: str
    artists: list[Artist]
    album: str
    cover_art: str
    preview: str
    user: str | None = None

@dataclass
class User(APIModel):
    name: str
    email: str
    id: str | None = None
    token: str = ''
    refresh_token: str = ''
    token_expires: str = ''
    top_tracks: list[Track] = field(default_factory=list)

    _client_cls: ClassVar[Type[Client]]

    def __post_init__(self) -> None:
        self._client = self._client_cls()

    def get_top_tracks(self, amount: int = 50) -> list[Track]:
        self.top_tracks = self._client.get_top_tracks_from_user(self, amount)
        for track in self.top_tracks:
            track.user = self.id
        return self.top_tracks

class Client(Protocol):
    """This is an interface for API Clients for music streaming services"""
    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError()
    
    def get_user(self, user_identifier: str) -> User:
        raise NotImplementedError()
    
    def get_top_tracks_from_user(self, user: User, amount: int = 50) -> list[Track]:
        raise NotImplementedError()