from dataclasses import dataclass
from typing import Protocol, Any, List, Self

SUCCESS_STATUSES = [200]

class APIModel:
    @classmethod
    def from_api_response(cls, response: dict[str, Any]) -> Self:
        raise NotImplementedError
    
@dataclass
class User(APIModel):
    name: str
    email: str

@dataclass
class Artist(APIModel):
    name: str
    url: str

@dataclass
class Track(APIModel):
    name: str
    url: str
    artists: list[Artist]
    album: str
    cover_art: str


class Client(Protocol):
    """This is an interface for API Clients for music streaming services"""
    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError()
    
    def get_user(self, user_identifier: str) -> User:
        raise NotImplementedError()
    
    def get_top_tracks_from_user(self, user_identifier: str, amount: int = 50) -> List[Track]:
        raise NotImplementedError()