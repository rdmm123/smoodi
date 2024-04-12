from flask import Blueprint, redirect, session, request, url_for, make_response
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode

from core.client.spotify_client import SpotifyClient
from core.helpers import get_random_string, get_absolute_url_for
from core.storage.session_storage import SessionStorage

bp = Blueprint('auth', __name__, url_prefix='/auth')
client = SpotifyClient()
storage = SessionStorage(session)

@bp.route("/login")
def login() -> ResponseReturnValue:
    state = get_random_string(16)
    
    auth_url = client.generate_auth_url(
        get_absolute_url_for('auth.callback'), state)
    
    session['state'] = state
    return redirect(auth_url)

@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for('frontend.catch_all')))
    session.clear()
    storage.flush()
    return resp

@bp.route("/callback")
def callback() -> ResponseReturnValue:
    code = request.args.get('code', '')
    state = request.args.get('state', '')
    error = request.args.get('error', '')

    if not state or state != session['state']:
        return redirect('/#?' + urlencode({
            'error': 'state_mismatch'
        }))
    
    if error and not code:
        return redirect('/#?' + urlencode({
            'error': error
        }))
    
    del session['state']
    
    auth_resp = client.authenticate(
        auth_code=code, redirect_url=get_absolute_url_for('auth.callback'))
    
    resp = make_response(redirect(url_for('frontend.catch_all')))
    
    storage.write('token', auth_resp['access_token'])
    storage.write('refresh', auth_resp['refresh_token'])
    storage.write('expires', str(auth_resp['expires_in']))

    return resp
