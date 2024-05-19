import datetime as dt
from flask import Blueprint, request, abort
from flask.typing import ResponseReturnValue

from src.backend import client, user_repository
from src.core.client.spotify.models import SpotifyPlaylist
from src.core.blender import Blender

KEYS_TO_EXLUDE_FROM_USER = ("token", "refresh_token", "token_expires", "top_tracks")

bp = Blueprint("blender", __name__, url_prefix="/blender")


@bp.route("/blend", methods=["POST"])
def blend() -> ResponseReturnValue:
    body = request.get_json()
    create = body.get("create", False)

    if "users" not in body or not body["users"]:
        abort(400, "Users not in request")

    users = user_repository.get_users(body["users"])

    for user in users:
        if not user or not user.id:
            abort(400, f"User {user} not found")

        new_auth_data = client.handle_token_refresh(
            user.token,
            user.refresh_token,
            dt.datetime.fromisoformat(user.token_expires),
        )

        if new_auth_data["refreshed"]:
            user.load_auth_data_from_response(new_auth_data)
            user_repository.save_user(user)

    if "playlist_length" in body and body["playlist_length"]:
        blender = Blender(client, users, body["playlist_length"])
    else:
        blender = Blender(client, users)

    tracks = blender.blend()
    playlist = SpotifyPlaylist(tracks=tracks)

    if create:
        playlist_name = "Blendify - " + ", ".join([u.name for u in users])
        playlist = client.create_playlist(
            user=user,
            name=playlist_name,
            public=False,
            collaborative=True,
            description=playlist_name,
        )
        client.update_playlist_tracks(user, playlist, tracks)

    return {"playlist": playlist}
