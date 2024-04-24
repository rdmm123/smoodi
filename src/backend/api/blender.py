import datetime as dt
from flask import Blueprint, request
from flask.typing import ResponseReturnValue

from core.client.spotify.spotify_client import SpotifyClient
from core.client.spotify.models import SpotifyUser
from core.storage.cache_storage import CacheStorage
from core.repositories.user_repository import UserRepository
from core.blender import Blender

KEYS_TO_EXLUDE_FROM_USER = ('token', 'refresh_token', 'token_expires', 'top_tracks')

client = SpotifyClient()
storage = CacheStorage()
user_repository = UserRepository(user_cls=SpotifyUser)

bp = Blueprint('blender', __name__, url_prefix='/blender')

@bp.route('/blend', methods=['POST'])
def blend() -> ResponseReturnValue:
    body = request.get_json()
    create = body.get('create', False)

    if 'users' not in body or not body['users']:
        return {
            'message': 'Users not in request'
        }, 400
    
    users = user_repository.get_users(body['users'])

    for user in users:
        if not user or not user.id:
            return {
                'message': f'User {user} not found'
            }, 400
    
        new_auth_data = client.handle_token_refresh(
            user.token,
            user.refresh_token,
            dt.datetime.fromisoformat(user.token_expires)
        )

        if new_auth_data['refreshed']:
            user.load_auth_data_from_response(new_auth_data)
            user_repository.save_user(user)


    blender = Blender(client, users)

    if 'playlist_length' in body and body['playlist_length']:
        blender.playlist_length = body['playlist_length']

    playlist = blender.blend(create=create)
    
    # Create playlist here
    return {
        'playlist': playlist
    }