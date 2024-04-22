import json
import datetime as dt
from flask import Blueprint, session
from dataclasses import asdict

from core.client.spotify.spotify_client import SpotifyClient, SpotifyUser
from core.storage.cache_storage import CacheStorage

client = SpotifyClient()
storage = CacheStorage()

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users/<user_email>')
def get_user(user_email: str):
    if user_email == 'me':
        user_email = session.get('email')

    user_raw = storage.read(f"user:{user_email}")

    if not user_raw:
        return {
            'message': f'User {user_email} not found!'
        }, 404
    
    user = json.loads(user_raw)
    user_obj = SpotifyUser(**user)
    new_auth_data = client.handle_token_refresh(user_obj.token,
                                user_obj.token_expires,
                                dt.datetime.fromisoformat(user_obj.token_expires))
        
    if new_auth_data['refreshed']:
        user_obj.load_auth_data_from_response(new_auth_data)
        storage.write(f'user:{user_obj.email}', json.dumps(asdict(user)))

    return {
        'user': asdict(user_obj)
    }

@bp.route('')
def user_session():
    pass