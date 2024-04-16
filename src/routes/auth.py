import base64
import click
import json
import time
import datetime as dt
from flask import Blueprint, redirect, session, request, url_for, make_response
from flask.typing import ResponseReturnValue
from urllib.parse import urlencode
from dataclasses import asdict

from core.client.spotify.spotify_client import SpotifyClient
from core.client.spotify.models import SpotifyUser
from core.helpers import get_random_string, get_absolute_url_for, is_email_valid
from core.storage.cache_storage import CacheStorage
from core.blender import Blender

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
    
    user = client.get_user(auth_resp['token'])
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

@bp.cli.command('auth-flow')
def auth_flow() -> None:
    def check_for_user_login(email: str, attempts: int = 60, sleep_seconds: int = 1) -> bool:
        user_logged_in = False
        attempt_count = 0

        click.echo("Waiting for log in... "
                    f"(You have {attempts * sleep_seconds} seconds)")
        
        while not user_logged_in and attempt_count < attempts:
            time.sleep(sleep_seconds)
            user_data = storage.read(f'user:{email}')
            user_logged_in = user_data is not None
            attempt_count += 1

        return user_logged_in
    users: list[SpotifyUser] = []
    
    login_url = url_for('auth.login')

    # this is just to check if user logged in. we don't really need it.
    main_user_email = click.prompt("What's your spotify email?", type=str)
    click.echo(f"Please log in using this link: {login_url}")

    if not check_for_user_login(main_user_email):
        return
    
    users.append(SpotifyUser(**json.loads(storage.read(f'user:{main_user_email}'))))

    click.echo("Now to add the rest of the users to the blend...")
    add_new_user = True
    while add_new_user:
        new_user_email = click.prompt("What's your friend's email?", type=str)

        if not is_email_valid(new_user_email):
            click.echo("Invalid email. Please try again.")
            continue
        
        encoded_email = base64.urlsafe_b64encode(
            new_user_email.encode()).decode()
        
        click.echo(f"Please send this link to your friend to log in: {login_url + '/' + encoded_email}")

        if not check_for_user_login(new_user_email):
            return
        
        users.append(SpotifyUser(**json.loads(storage.read(f'user:{new_user_email}'))))

        add_new_user = click.confirm("Do you wish to add another user?")

    length = click.prompt("Length of playlist?", type=int)
    blender = Blender(client, users, length)
    playlist = blender.blend()
    click.echo(playlist)