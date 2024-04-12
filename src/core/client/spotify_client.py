import os
import requests
import base64
from urllib.parse import urlencode
from typing import Dict, Any

from core.helpers import get_missing_keys
from core.client.client import Client


class SpotifyClient(Client):
    SPOTIFY_AUTH_URL = 'https://accounts.spotify.com'
    SPOTIFY_API_URL = 'https://api.spotify.com/v1'

    SCOPES = (
        'playlist-read-private',
        'playlist-read-collaborative',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-top-read',
        'user-read-email'
    )

    client_secret = None
    client_id = None

    # The keys here will end up being class attributes
    load_from_env = {
        'client_secret': 'SPOTIFY_CLIENT_SECRET',
        'client_id': 'SPOTIFY_CLIENT_ID'
    }

    def __init__(self) -> None:
        self._load_attrs_from_env()

    def _load_attrs_from_env(self) -> None:
        for attribute, env_var in self.load_from_env.items():
            value = os.getenv(env_var)

            if value is None:
                raise Exception(f'{env_var} not found in environment variables.')
            
            setattr(self, attribute, value)

    def generate_auth_url(self, redirect_url: str, state: str | None = None) -> str:
        query_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': ' '.join(self.SCOPES),
            'show_dialog': False
        }

        if state is not None:
            query_params['state'] = state

        return f'{self.SPOTIFY_AUTH_URL}/authorize?{urlencode(query_params)}'
    
    def authenticate(self, **kwargs: Any) -> Dict[str, Any]:
        auth_code = kwargs.get('auth_code')
        redirect_url = kwargs.get('redirect_url')
        
        body = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_url
        }
        b64_auth_string = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode()).decode()
        headers = {
            'Authorization': f'Basic {b64_auth_string}'
        }
        r = requests.post(f'{self.SPOTIFY_AUTH_URL}/api/token',
                             data=body,
                             headers=headers)
        resp: Dict[str, Any] = r.json()

        missing_keys = get_missing_keys(
            resp, 'access_token', 'refresh_token', 'expires_in')

        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found in response."
                            f"\nresponse: {resp}\nrequest body: {body}"
                            f"\nrequest_headers: {headers}")
        
        return resp