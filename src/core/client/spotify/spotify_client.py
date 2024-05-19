import datetime as dt
import requests
import base64
import json
from urllib.parse import urlencode
from typing import Any, Iterable
from flask import current_app
from collections.abc import Sequence

from src.core.helpers import get_missing_keys, LoadFromEnvMixin, truncate_text
from src.core.client.base import Client, SUCCESS_STATUSES, Track, User, Playlist
from src.core.client.spotify.models import SpotifyUser, SpotifyTrack, SpotifyPlaylist
from src.core.storage.base import Storage


# TODO: use cache to save requests made
class SpotifyClient(LoadFromEnvMixin, Client):
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com"
    SPOTIFY_API_URL = "https://api.spotify.com/v1"

    SCOPES = (
        "playlist-read-private",
        "playlist-read-collaborative",
        "playlist-modify-private",
        "playlist-modify-public",
        "user-top-read",
        "user-read-email",
    )

    client_secret = None
    client_id = None

    load_from_env = {
        "client_secret": "SPOTIFY_CLIENT_SECRET",
        "client_id": "SPOTIFY_CLIENT_ID",
    }

    CACHE_KEY_PREFIX = "spotify_api_request:"
    CACHE_EXPIRY = 3540  # tokens expire in an hour, so should all data

    def __init__(self, storage: Storage) -> None:
        self._storage = storage
        super().__init__()

    def _make_request(
        self, method: str, keys_to_check: Iterable[str] = [], **request_kwargs: Any
    ) -> dict[str, Any]:
        current_app.logger.info(
            f"{method.upper()} Request to Spotify API: {truncate_text(str(request_kwargs), 300)}"
        )

        if method.lower() == "get":
            cached_response = self._get_response_from_cache(
                method=method, **request_kwargs
            )
            if cached_response:
                current_app.logger.info(
                    f"{method.upper()} Response retrieved from cache: {truncate_text(str(cached_response), 300)}"
                )
                return cached_response

        r = requests.request(method.upper(), **request_kwargs)

        current_app.logger.info(
            f"{r.status_code} Response from Spotify API: {truncate_text(r.text, 300)}"
        )

        if r.status_code not in SUCCESS_STATUSES:
            raise Exception(f"Error {r.status_code} received from Spotify API")

        resp: dict[str, Any] = r.json()

        if method.lower() == "get":
            self._save_response_to_cache(resp, method=method, **request_kwargs)

        missing_keys = get_missing_keys(resp, *keys_to_check)
        if missing_keys:
            raise Exception(f"{', '.join(missing_keys)} not found in response.")

        return resp

    def _get_response_from_cache(self, **request_kwargs: Any) -> dict[str, Any] | None:
        key = self._get_cache_key_for_request(request_kwargs)
        response_raw: str | None = self._storage.read(key)

        if response_raw:
            response: dict[str, Any] = json.loads(response_raw)
            return response

        return None

    def _save_response_to_cache(
        self, response: dict[str, Any], **request_kwargs: Any
    ) -> None:
        key = self._get_cache_key_for_request(request_kwargs)
        self._storage.write(key, json.dumps(response), expiry_seconds=self.CACHE_EXPIRY)

    def _get_cache_key_for_request(self, request_kwargs: dict[str, Any]) -> str:
        cache_key_list = [f"{k}:{v}" for k, v in request_kwargs.items()]
        return self.CACHE_KEY_PREFIX + ":".join(cache_key_list)

    def generate_auth_url(self, redirect_url: str, state: str | None = None) -> str:
        query_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_url,
            "scope": " ".join(self.SCOPES),
            "show_dialog": False,
        }

        if state is not None:
            query_params["state"] = state

        return f"{self.SPOTIFY_AUTH_URL}/authorize?{urlencode(query_params)}"

    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        auth_code = kwargs.get("auth_code")
        redirect_url = kwargs.get("redirect_url")

        body = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_url,
        }
        b64_auth_string = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {"Authorization": f"Basic {b64_auth_string}"}

        keys_to_check = ("access_token", "refresh_token", "expires_in")
        resp = self._make_request(
            method="post",
            keys_to_check=keys_to_check,
            url=f"{self.SPOTIFY_AUTH_URL}/api/token",
            data=body,
            headers=headers,
        )

        expiry_date = dt.datetime.now() + dt.timedelta(seconds=resp["expires_in"])
        return {
            "token": resp["access_token"],
            "refresh_token": resp["refresh_token"],
            "expiry_date": expiry_date,
        }

    def handle_token_refresh(
        self, token: str, refresh_token: str, expiry_date: dt.datetime
    ) -> dict[str, Any]:
        if dt.datetime.now() < expiry_date:
            return {"token": token, "expiry_date": expiry_date, "refreshed": False}

        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }
        b64_auth_string = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        headers = {"Authorization": f"Basic {b64_auth_string}"}

        keys_to_check = ("access_token", "expires_in")
        resp = self._make_request(
            method="post",
            keys_to_check=keys_to_check,
            url=f"{self.SPOTIFY_AUTH_URL}/api/token",
            data=body,
            headers=headers,
        )

        new_expiry_date = dt.datetime.now() + dt.timedelta(seconds=resp["expires_in"])
        return {
            "token": resp["access_token"],
            "expiry_date": new_expiry_date,
            "refreshed": True,
        }

    def get_user(self, user_identifier: str) -> SpotifyUser:
        resp = self._make_request(
            method="get",
            url=f"{self.SPOTIFY_API_URL}/me",
            headers={"Authorization": f"Bearer {user_identifier}"},
        )
        return SpotifyUser.from_api_response(resp)

    def get_top_tracks_from_user(
        self, user: User, amount: int = 50
    ) -> list[SpotifyTrack]:
        # could move pagination logic to _make_request
        offset = 0
        max_limit = 50
        remaining = amount
        time_range = "short_term"

        tracks: list[SpotifyTrack] = []
        while remaining > 0:
            limit = remaining if remaining < max_limit else max_limit

            query_params = {
                "time_range": time_range,  # TODO: make this customizable
                "limit": limit,
                "offset": offset,
            }

            resp = self._make_request(
                method="get",
                url=f"{self.SPOTIFY_API_URL}/me/top/tracks",
                params=query_params,
                headers={"Authorization": f"Bearer {user.token}"},
            )

            # TODO: Make it so that we use all of the ones for last mont first
            # And then fill in the rest with 6 months. Could do the following logic:
            # Simply check if the list if empty (it'll get to that point lol)
            # and then retry using the following term 'medium_term'
            if resp["total"] < amount:
                current_app.logger.info(
                    f"User {user.email}'s top tracks from last month arent enough."
                    f"Amount requested: {amount}, total: {resp['total']}."
                )
                time_range = "medium_term"
                continue

            for track in resp["items"]:
                track_obj = SpotifyTrack.from_api_response(track)
                track_obj.user = user.id
                tracks.append(track_obj)

            offset += limit
            remaining -= limit

        return tracks

    def create_playlist(
        self,
        *,
        user: User,
        name: str,
        public: bool,
        collaborative: bool,
        description: str,
    ) -> SpotifyPlaylist:
        resp = self._make_request(
            "post",
            ["id"],
            url=f"{self.SPOTIFY_API_URL}/users/{user.api_id}/playlists",
            json={
                "name": name,
                "public": public,
                "collaborative": collaborative,
                "description": description,
            },
            headers={"Authorization": f"Bearer {user.token}"},
        )

        return SpotifyPlaylist.from_api_response(resp)

    def update_playlist_tracks(
        self, user: User, playlist: Playlist, tracks: Sequence[Track]
    ) -> Playlist:
        url = f"{self.SPOTIFY_API_URL}/playlists/{playlist.id}/tracks"
        max_limit = 100
        track_uris = [t.uri for t in tracks]
        uris_replace = track_uris[:max_limit]
        uris_add = track_uris[max_limit:]

        self._make_request(
            "put",
            ["snapshot_id"],
            url=url,
            json={"uris": uris_replace},
            headers={"Authorization": f"Bearer {user.token}"},
        )

        while uris_add:
            uris_to_send = uris_add[:max_limit]
            uris_add = uris_add[max_limit:]

            self._make_request(
                "post",
                ["snapshot_id"],
                url=url,
                json={"uris": uris_to_send},
                headers={"Authorization": f"Bearer {user.token}"},
            )

        playlist.tracks = tracks
        return playlist
