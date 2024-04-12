import json
from flask import Blueprint, redirect, session, request, url_for, make_response
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode

from core.client.spotify_client import SpotifyClient
from core.helpers import get_random_string, get_absolute_url_for
from core.storage.session_storage import SessionStorage
from core.storage.cookie_storage import CookieStorage

bp = Blueprint('auth', __name__, url_prefix='/auth')
client = SpotifyClient()
storage = CookieStorage()

@bp.route("/login")
@bp.route("/login/external")
def login() -> ResponseReturnValue:
    # TODO: check if user credentials are stored before attempting login
    # TODO: Might need to pass the user's email in the route (b64 encoded)
    # to validate that /external is not being called arbitrarily
    # And then validate if the email passed in the url matches the one coming
    # from spotify
    state = get_random_string(16)
    
    auth_url = client.generate_auth_url(
        get_absolute_url_for('auth.callback'), state)
    
    session['state'] = state
    session['external'] = 'external' in request.path
    return redirect(auth_url)

@bp.route("/logout")
def logout() -> ResponseReturnValue:
    resp = make_response(redirect(url_for('frontend.catch_all')))
    storage.flush(response=resp)
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
    
    auth_resp = client.authenticate(
        auth_code=code, redirect_url=get_absolute_url_for('auth.callback'))
    
    redirect_to = url_for('frontend.catch_all')
    if session['external']:
        redirect_to = redirect_to + 'thanks/'
    
    resp = make_response(redirect(redirect_to))

    data = {k: str(auth_resp[k]) for k in ('access_token', 'expires_in', 'refresh_token')}
    
    storage.write('auth_data', json.dumps(data), response=resp)

    del session['state']
    del session['external']

    return resp
