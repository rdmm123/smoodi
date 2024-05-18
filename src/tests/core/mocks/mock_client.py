from typing import Any
from collections.abc import Sequence
from pathlib import Path
import json

from src.core.client.base import User, Playlist, Track, Artist

class MockClient:
    """Mocks an API client. Works by using the responses stored in the response folder."""
    def authenticate(self, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError()
    
    def get_user(self, user_identifier: str) -> User:
        raise NotImplementedError()
    
    def get_top_tracks_from_user(self, user: User, amount: int = 50) -> Sequence[Track]:
        assert user.id is not None
        responses_folder = Path('src/tests/core/mocks/responses')
        response_file = responses_folder / f"{user.id}.json"

        if not response_file.exists():
            raise ValueError(f'Response file not found {user.id}.json')
        
        with response_file.open() as f:
            response = json.load(f)

        tracks = []
        for track_json in response:
            artists = [Artist(**a) for a in track_json['artists']]
            track_json['artists'] = artists
            track = Track(**track_json)
            tracks.append(track)
        
        return tracks
    
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