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

# Consider not requiring email for secondary users
# In case main user doesn't know the email. I could link the link (lol) to the
# main user somehow instead. Or maybe create like a session code in which 
# people join? But obviously not known to people and just stored in the backend
# or maybe just do it hacky and have a set 'email' like 'unknown' and that way
# we know its not main user and we simply don't know the email for now
@bp.route("/login", defaults={'encoded_email': None})
@bp.route("/login/<encoded_email>")
def login(encoded_email: str | None) -> ResponseReturnValue:
    email = None
    existing_data = None
    if encoded_email:
        email = base64.urlsafe_b64decode(encoded_email + '==').decode()
        if not is_email_valid(email):
            return redirect(url_for('frontend.catch_all') + 'login_result?' + \
                            urlencode({'error': f'email {email} is not valid'}))
        existing_data = storage.read(f'user:{email}')
    
    if existing_data:
        user = SpotifyUser(**json.loads(existing_data))

        new_auth_data = client.handle_token_refresh(
            user.token,
            user.refresh_token,
            dt.datetime.fromisoformat(user.token_expires))
        
        if new_auth_data['refreshed']:
            user.load_auth_data_from_response(new_auth_data)
            storage.write(f'user:{user.email}', json.dumps(asdict(user)))
        
        session['email'] = user.email
        return redirect(url_for('frontend.catch_all'))

    state = get_random_string(16)
    auth_url = client.generate_auth_url(
        get_absolute_url_for('auth.callback'), state)
    
    session['state'] = state
    session['email'] = email

    return redirect(auth_url)

@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for('frontend.catch_all')))
    logged_in_user = session.get('email')
    if not logged_in_user:
        return resp
    storage.delete(f"user:{logged_in_user}")
    session.clear()
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
    
    user = client.get_user(auth_resp['token'])
    user.load_auth_data_from_response(auth_resp)
    
    if session['email'] and session['email'] != user.email:
        return redirect(redirect_to + '?' + urlencode({
            'error': 'email_mismatch'
        }))
    
    resp = make_response(redirect(redirect_to))
    storage.write(f'user:{user.email}', json.dumps(asdict(user)), response=resp)

    session['email'] = user.email
    del session['state']
    return resp
