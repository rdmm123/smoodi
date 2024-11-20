from dataclasses import dataclass
from typing import Dict, Any, Self
from flask import current_app

from src.core.client.base import User, Artist, Track, Playlist


@dataclass
class SpotifyUser(User):
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> Self:
        current_app.logger.info(f'Users images {response["images"]=}')
        return cls(
            name=response["display_name"],
            email=response["email"],
            api_id=response["id"],
            image_url=response["images"][0]["url"] if len(response["images"]) > 0 else "",
        )

    def load_auth_data_from_response(self, auth_response: Dict[str, Any]) -> None:
        if "token" in auth_response:
            self.token = auth_response["token"]
        if "refresh_token" in auth_response:
            self.refresh_token = auth_response["refresh_token"]
        if "expiry_date" in auth_response:
            self.token_expires = auth_response["expiry_date"].isoformat()


@dataclass
class SpotifyArtist(Artist):
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> Self:
        return cls(name=response["name"], url=response["external_urls"]["spotify"])


@dataclass
class SpotifyTrack(Track):
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> Self:
        return cls(
            name=response["name"],
            external_url=response["external_urls"]["spotify"],
            uri=response["uri"],
            artists=[
                SpotifyArtist.from_api_response(a) for a in response["album"]["artists"]
            ],
            album=response["album"]["name"],
            cover_art=response["album"]["images"][0]["url"] if len(response["album"]["images"]) > 0 else "",
            preview=response["preview_url"],
        )


@dataclass
class SpotifyPlaylist(Playlist):
    @classmethod
    def from_api_response(cls, response: Dict[str, Any]) -> Self:
        return cls(
            id=response["id"],
            href=response["href"],
            uri=response["uri"],
            name=response["name"],
            description=response["description"],
            external_url=response["external_urls"]["spotify"],
            owner=response["owner"]["display_name"],
            tracks=[
                SpotifyTrack.from_api_response(t["track"])
                for t in response["tracks"]["items"]
            ],
            public=response["public"],
            collaborative=response["collaborative"],
        )
