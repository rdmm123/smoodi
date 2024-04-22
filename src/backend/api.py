import datetime as dt
from flask import Blueprint, session
from flask.typing import ResponseReturnValue
from dataclasses import asdict

from core.client.spotify.spotify_client import SpotifyClient
from core.client.spotify.models import SpotifyUser
from core.storage.cache_storage import CacheStorage
from core.repositories.user_repository import UserRepository, InvalidUserException

client = SpotifyClient()
storage = CacheStorage()
user_repository = UserRepository(user_cls=SpotifyUser)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users/<user_email>')
def get_user(user_email: str) -> ResponseReturnValue:
    if user_email == 'me':
        user_email = session.get('email', '')

    try:
        user = user_repository.get_user(user_email)
    except InvalidUserException:
        return {
            'message': f'User {user_email} data has an invalid format.'
        }, 400

    if not user:
        return {
            'message': f'User {user_email} not found!'
        }, 404
    
    new_auth_data = client.handle_token_refresh(user.token,
                                user.token_expires,
                                dt.datetime.fromisoformat(user.token_expires))
        
    if new_auth_data['refreshed']:
        user.load_auth_data_from_response(new_auth_data)
        user_repository.save_user(user)

    user_dict = asdict(user)
    for key in ('token', 'refresh_token', 'token_expires'):
        del user_dict[key]

    return {
        'user': user_dict
    }

@bp.route('/users/<user_email>/session')
def user_session(user_email: str) -> ResponseReturnValue:
    return ""