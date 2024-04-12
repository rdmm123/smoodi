import datetime as dt
from dataclasses import dataclass
from typing import Dict, Any, Self

from core.client.base import User

@dataclass
class SpotifyUser(User):
    token: str | None = None
    refresh_token: str | None = None
    token_expires: str | None = None

    @classmethod
    def from_user_api_response(cls, response: Dict[str, Any]) -> Self:
        return cls(
            name=response['display_name'],
            email=response['email']
        )
    
    def load_auth_data_from_response(self, auth_response: Dict[str, Any]) -> None:
        self.token = auth_response['access_token']
        self.refresh_token = auth_response['refresh_token']
        expiry_date = dt.datetime.now() + dt.timedelta(seconds=auth_response['expires_in'])
        self.token_expires = expiry_date.isoformat()