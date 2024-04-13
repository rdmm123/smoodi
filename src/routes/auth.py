import json
import base64
from flask import Blueprint, redirect, session, request, url_for, make_response, current_app
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode
from dataclasses import asdict

from core.client.spotify.spotify_client import SpotifyClient
from core.helpers import get_random_string, get_absolute_url_for, is_email_valid
from core.storage.session_storage import SessionStorage
from core.storage.cookie_storage import CookieStorage
from core.storage.cache_storage import CacheStorage

bp = Blueprint('auth', __name__, url_prefix='/auth')
client = SpotifyClient()
storage = CacheStorage()

@bp.route("/login", defaults={'encoded_email': None})
@bp.route("/login/<encoded_email>")
def login(encoded_email: str | None) -> ResponseReturnValue:
    state = get_random_string(16)
    
    email = None
    existing_data = None
    if encoded_email:
        email = base64.urlsafe_b64decode(encoded_email).decode()
        if not is_email_valid(email):
            return redirect(url_for('frontend.catch_all') + 'login_result?' + \
                            urlencode({'error': f'email {email} is not valid'}))
        current_app.logger.debug(request.cookies)
        existing_data = storage.read(f'user:{email}')
    
    if existing_data:
        return redirect(url_for('frontend.catch_all'))

    session['email'] = email

    auth_url = client.generate_auth_url(
        get_absolute_url_for('auth.callback'), state)
    
    session['state'] = state
    return redirect(auth_url)

@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for('frontend.catch_all')))
    session.clear()
    storage.flush(response=resp)
    return resp

@bp.route("/callback")
def callback() -> ResponseReturnValue:
    code = request.args.get('code', '')
    state = request.args.get('state', '')
    error = request.args.get('error', '')

    redirect_to = url_for('frontend.catch_all') + 'login_result/'

    if not state or state != session['state']:
        del session['state']
        del session['email']
        return redirect(redirect_to + '?' + urlencode({
            'error': 'state_mismatch'
        }))
    
    if error and not code:
        del session['state']
        del session['email']
        return redirect(redirect_to + '?' + urlencode({
            'error': error
        }))
    
    auth_resp = client.authenticate(
        auth_code=code, redirect_url=get_absolute_url_for('auth.callback'))
    
    user = client.get_user(auth_resp['access_token'])
    user.load_auth_data_from_response(auth_resp)
    
    if session['email'] and session['email'] != user.email:
        return redirect(redirect_to + '?' + urlencode({
            'error': 'email_mismatch'
        }))
    
    resp = make_response(redirect(redirect_to))
    storage.write(f'user:{user.email}', json.dumps(asdict(user)), response=resp)

    del session['state']
    del session['email']
    return resp
