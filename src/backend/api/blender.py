import datetime as dt
from flask import Blueprint, request, abort, current_app


from flask.typing import ResponseReturnValue
from typing import Any

from src.backend import client, user_repository
from src.core.client.spotify.models import SpotifyPlaylist
from src.core.blender import Blender

KEYS_TO_EXLUDE_FROM_USER = ("token", "refresh_token", "token_expires", "top_tracks")

bp = Blueprint("blender", __name__, url_prefix="/blender")


@bp.route("/preview", methods=["POST"])
def blend() -> ResponseReturnValue:
    body = request.get_json()
    shuffle = body.get("shuffle", False)
    main_user_id = body.get("main_user", None)
    session_ids = body.get("session", None)

    if "main_user" not in body or not body["main_user"]:
        abort(400, "Main user not provided")

    if "session" not in body or not body["session"]:
        abort(400, "Session not provided")

    users = user_repository.get_users([main_user_id] + session_ids)

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

    tracks = blender.blend(shuffle)
    user_repository.save_blend(main_user_id, tracks)
    playlist = SpotifyPlaylist(tracks=tracks)

    return {"playlist": playlist}


@bp.route("/create", methods=["POST"])
def create_blend() -> ResponseReturnValue:
    body: dict[str, Any] = request.get_json()
    user_id: str | None = body.get("user", None)

    if not user_id:
        abort(400, "User not in request")

    main_user = user_repository.get_user(user_id)
    session = user_repository.get_user_session(user_id)

    current_app.logger.debug(f"IM THE MAIN USER {main_user=} {user_id=}")
    for user in [main_user] + session:
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

    tracks = user_repository.get_blend(user_id)

    if not tracks:
        abort(
            400,
            "Looks like there is no preview stored, remember to preview your playlist before creating.",
        )

    assert main_user
    playlist_name = f"Smoodi - {main_user.name}{', '.join([u.name for u in session])}"
    playlist = client.create_playlist(
        user=main_user,
        name=playlist_name,
        public=False,
        collaborative=True,
        description=playlist_name,
    )
    client.update_playlist_tracks(main_user, playlist, tracks)

    return {"playlist": playlist}
