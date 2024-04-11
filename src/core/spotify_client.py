import os
import requests
import base64
from urllib.parse import urlencode

from core.helpers import get_missing_keys


class SpotifyClient:
    SPOTIFY_BASE_URL = 'https://accounts.spotify.com'
    SPOTIFY_API_URL = SPOTIFY_BASE_URL + '/api'

    SCOPES = (
        'playlist-read-private',
        'playlist-read-collaborative',
        'playlist-modify-private',
        'playlist-modify-public',
        'user-top-read',
        'user-read-email'
    )

    client_secret = 'SPOTIFY_CLIENT_SECRET'
    client_id = 'SPOTIFY_CLIENT_ID'

    _load_from_env = ['client_secret', 'client_id']

    def __init__(self) -> None:
        self._load_attrs_from_env()

    def _load_attrs_from_env(self):
        for attribute in self._load_from_env:
            env_var = getattr(self, attribute)
            value = os.getenv(env_var)

            if value is None:
                raise Exception(f'{env_var} not found in environment variables.')
            
            setattr(self, attribute, value)

    def generate_auth_url(self, redirect_url: str, state: str | None = None):
        query_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'scope': ' '.join(self.SCOPES)
        }

        if state is not None:
            query_params['state'] = state

        return f'{self.SPOTIFY_BASE_URL}/authorize?{urlencode(query_params)}'
    
    def authenticate(self, auth_code: str, redirect_url: str):
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
        r = requests.post(f'{self.SPOTIFY_API_URL}/token',
                             data=body,
                             headers=headers)
        resp = r.json()

        missing_keys = get_missing_keys(
            resp, 'access_token', 'refresh_token', 'expires_in')

        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found in response."
                            f"\nresponse: {resp}\nrequest body: {body}"
                            f"\nrequest_headers: {headers}")
        
        return resp