from flask import Blueprint, redirect, session, request, url_for, make_response
from urllib.parse import urlencode

from core.spotify_client import SpotifyClient
from core.helpers import get_random_string, get_absolute_url_for

bp = Blueprint('api', __name__, url_prefix='/api')
spotify_client = SpotifyClient()

@bp.route("/auth")
def auth():
    state = get_random_string(16)

    
    auth_url = spotify_client.generate_auth_url(
        get_absolute_url_for('api.callback'), state)
    
    session['state'] = state
    return redirect(auth_url)

@bp.route("/callback")
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')

    if not state or state != session['state']:
        return redirect('/#?' + urlencode({
            'error': 'state_mismatch'
        }))
    
    if error and not code:
        return redirect('/#?' + urlencode({
            'error': error
        }))
    
    del session['state']
    
    auth_resp = spotify_client.authenticate(
        code, get_absolute_url_for('api.callback'))
    
    resp = make_response(redirect(url_for('catch_all.catch_all')))
    resp.set_cookie('token', auth_resp['access_token'])
    resp.set_cookie('refresh', auth_resp['refresh_token'])
    resp.set_cookie('expires', str(auth_resp['expires_in']))

    return resp
