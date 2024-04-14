import datetime as dt
from dataclasses import dataclass
from typing import Dict, Any, Self

from core.client.base import User

@dataclass
class SpotifyUser(User):
    token: str = ''
    refresh_token: str = ''
    token_expires: str = ''

    @classmethod
    def from_user_api_response(cls, response: Dict[str, Any]) -> Self:
        return cls(
            name=response['display_name'],
            email=response['email']
        )
    
    def load_auth_data_from_response(self, auth_response: Dict[str, Any]) -> None:
        if 'token' in auth_response:
            self.token = auth_response['token']
        if 'refresh_token' in auth_response:
            self.refresh_token = auth_response['refresh_token']
        if 'expiry_date' in auth_response:
            self.token_expires = auth_response['expiry_date'].isoformat()