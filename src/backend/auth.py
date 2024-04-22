import base64
import json

import datetime as dt
from flask import Blueprint, redirect, session, request, url_for, make_response
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode
from dataclasses import asdict

from core.client.spotify.spotify_client import SpotifyClient
from core.client.spotify.models import SpotifyUser
from core.helpers import get_random_string, get_absolute_url_for, is_email_valid
from core.storage.cache_storage import CacheStorage

bp = Blueprint('auth', __name__, url_prefix='/auth')
client = SpotifyClient()
storage = CacheStorage()

@bp.route("/login", defaults={'encoded_email': None})
@bp.route("/login/<encoded_email>")
def login(encoded_email: str | None) -> ResponseReturnValue:
    if encoded_email is not None: # Link is shared by the user creating the blend (main user)
        main_user_email = base64.urlsafe_b64decode(encoded_email + '==').decode()
        if not is_email_valid(main_user_email):
            return redirect(url_for('frontend.catch_all') + '?' +
                            urlencode({'error': f'email {main_user_email} is not valid'}))
        
        existing_data = storage.read(f'user:{main_user_email}')
        if not existing_data:
            return redirect(url_for('frontend.catch_all') + '?' +
                            urlencode({'error': 'Main user not logged in.'}))
        session['main_user_email'] = main_user_email

    state = get_random_string(16)
    auth_url = client.generate_auth_url(
        get_absolute_url_for('auth.callback'), state)
    
    session['state'] = state
    return redirect(auth_url)

@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for('frontend.catch_all')))
    logged_in_user = session.get('email')
    if not logged_in_user:
        return resp
    storage.delete(f"user:{logged_in_user}")
    storage.delete(f"session:{logged_in_user}")
    session.clear()
    return resp

@bp.route("/callback")
def callback() -> ResponseReturnValue:
    code = request.args.get('code', '')
    state = request.args.get('state', '')
    error = request.args.get('error', '')

    redirect_to = url_for('frontend.catch_all')

    if not state or state != session['state']:
        del session['state']
        if 'main_user_email' in session:
            del session['main_user_email']
        return redirect(redirect_to + '?' + urlencode({
            'error': 'state_mismatch'
        }))
    
    if error and not code:
        del session['state']
        if 'main_user_email' in session:
            del session['main_user_email']
        return redirect(redirect_to + '?' + urlencode({
            'error': error
        }))
    
    auth_resp = client.authenticate(
        auth_code=code, redirect_url=get_absolute_url_for('auth.callback'))
    
    user = client.get_user(auth_resp['token'])
    user.load_auth_data_from_response(auth_resp)
    
    resp = make_response(redirect(redirect_to))
    storage.write(f'user:{user.email}', json.dumps(asdict(user)), response=resp)

    del session['state']

    if 'main_user_email' in session:
        current_session_key = f"session:{session['main_user_email']}"
        current_session: list = json.loads(storage.read(current_session_key) or '[]')

        if user.email not in current_session:
            current_session.append(user.email)
            storage.write(f'session:{session['main_user_email']}', json.dumps(current_session))

        del session['main_user_email']
        return resp # TODO: change to redirect to login_result

    session['email'] = user.email
    return resp
