from typing import Protocol, Any, Dict

class Client(Protocol):
    """This is an interface for API Clients for music streaming services"""
    def authenticate(self, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError()
    
    def get_user(self, user_identifier: str) -> Dict[str, Any]:
        raise NotImplementedError()
    
    def get_top_tracks_from_user(self, user_identifier: str) -> Dict[str, Any]:
        raise NotImplementedError()