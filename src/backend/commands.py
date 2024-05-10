import click
import time
import json
import base64
import datetime as dt
from flask import url_for, Blueprint
from dataclasses import asdict

from src.backend import user_repository, client
from src.core.client.spotify.models import SpotifyUser
from src.core.helpers import is_email_valid
from src.core.blender import Blender

bp = Blueprint('commands', __name__)
@bp.cli.command('test-app-flow')
def test_app_flow() -> None:
    def check_for_user_login(email: str, attempts: int = 60, sleep_seconds: int = 1) -> bool:
        user_logged_in = False
        attempt_count = 0

        click.echo("Waiting for log in... "
                    f"(You have {attempts * sleep_seconds} seconds)")
        
        while not user_logged_in and attempt_count < attempts:
            time.sleep(sleep_seconds)
            user = user_repository.get_user(email)

            if user is None:
                user_logged_in = False
                continue

            token_expired = dt.datetime.now() > dt.datetime.fromisoformat(user.token_expires)

            user_logged_in = not token_expired
            attempt_count += 1

        return user_logged_in
    
    users: list[SpotifyUser] = []
    
    login_url = url_for('auth.login')

    # this is just to check if user logged in. we don't really need it.
    main_user_email = click.prompt("What's your spotify email?", type=str)
    click.echo(f"Please log in using this link: {login_url}")

    if not check_for_user_login(main_user_email):
        return

    main_user = user_repository.get_user(main_user_email)
    if main_user is not None:
        users.append(main_user)

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
        
        new_user = user_repository.get_user(new_user_email)
        if new_user is not None:
            users.append(new_user)

        add_new_user = click.confirm("Do you wish to add another user?")

    length = click.prompt("Length of playlist?", type=int)
    blender = Blender(client, users, length)
    playlist = blender.blend()
    playlist_dict = [asdict(track) for track in playlist]
    click.echo(json.dumps(playlist_dict))