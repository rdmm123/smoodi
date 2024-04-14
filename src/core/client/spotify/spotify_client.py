import os
import requests
import base64
from urllib.parse import urlencode
from typing import Dict, Any
from flask import current_app

from core.helpers import get_missing_keys, LoadFromEnvMixin
from core.client.base import Client
from core.client.spotify.spotify_user_model import SpotifyUser


class SpotifyClient(Client, LoadFromEnvMixin):
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

    load_from_env = {
        'client_secret': 'SPOTIFY_CLIENT_SECRET',
        'client_id': 'SPOTIFY_CLIENT_ID'
    }

    def _make_request(self, method: str, **request_kwargs: Any) -> Dict[str, Any]:
        current_app.logger.debug(f'{method.upper()} Request to Spotify API: {request_kwargs}')
        r = requests.request(method.upper(), **request_kwargs)
        current_app.logger.debug(f'{r.status_code} Response from Spotify API: {r.text}')
        resp: Dict[str, Any] = r.json()
        return resp

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

        resp = self._make_request('post', 
                                  url=f'{self.SPOTIFY_AUTH_URL}/api/token',
                                  data=body,
                                  headers=headers)

        missing_keys = get_missing_keys(
            resp, 'access_token', 'refresh_token', 'expires_in')

        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found in response."
                            f"\nresponse: {resp}\nrequest body: {body}"
                            f"\nrequest_headers: {headers}")
        
        return resp
    
    def get_user(self, user_identifier: str) -> SpotifyUser:        
        resp = self._make_request(
            method='get',
            url=f'{self.SPOTIFY_API_URL}/me',
            headers={'Authorization': f'Bearer {user_identifier}'})
        return SpotifyUser.from_user_api_response(resp)