from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, Any, Self, ClassVar, Type, TypeVar
from collections.abc import Sequence

SUCCESS_STATUSES = [200, 201]

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
    artists: Sequence[Artist]
    album: str
    cover_art: str
    preview: str
    user: str | None = None

@dataclass
class User(APIModel):
    name: str
    email: str
    api_id: str
    id: str | None = None
    token: str = ''
    refresh_token: str = ''
    token_expires: str = ''
    top_tracks: Sequence[Track] = field(default_factory=list)

    _client_cls: ClassVar[Type[Client]]

    def __post_init__(self) -> None:
        self._client = self._client_cls()

    def get_top_tracks(self, amount: int = 50) -> Sequence[Track]:
        self.top_tracks = self._client.get_top_tracks_from_user(self, amount)
        for track in self.top_tracks:
            track.user = self.id
        return self.top_tracks
    
@dataclass
class Playlist(APIModel):
    tracks: Sequence[Track]
    id: str = ''
    href: str = ''
    uri: str = ''
    external_url: str = ''
    name: str = ''
    description: str = ''
    owner: str = ''
    public: bool = False
    collaborative: bool = False


class Client(Protocol):
    """This is an interface for API Clients for music streaming services"""
    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError()
    
    def get_user(self, user_identifier: str) -> User:
        raise NotImplementedError()
    
    def get_top_tracks_from_user(self, user: User, amount: int = 50) -> Sequence[Track]:
        raise NotImplementedError()
    
    def create_playlist(self,
                        *,
                        user: User,
                        name: str,
                        public: bool,
                        collaborative: bool,
                        description: str) -> Playlist:
        raise NotImplementedError()
    
    def update_playlist_tracks(self, user: User, playlist: Playlist, tracks: Sequence[Track]) -> Playlist:
        raise NotImplementedError()