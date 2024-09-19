import datetime as dt
from flask import Blueprint, session, abort
from flask.typing import ResponseReturnValue
from dataclasses import asdict

from src.backend import user_repository, client
from src.core.repositories.user_repository import InvalidJsonException
from src.core.client.spotify.models import SpotifyUser

KEYS_TO_EXCLUDE_FROM_USER = ("token", "refresh_token", "token_expires")

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/<user_id>")
def get_user(user_id: str) -> ResponseReturnValue:
    if user_id == "me":
        user_id = session.get("user_id", "")

    try:
        user = user_repository.get_user(user_id)
    except InvalidJsonException:
        abort(400, f"User {user_id} data has an invalid format.")

    if not user:
        abort(404, f"User {user_id} not found!")

    new_auth_data = client.handle_token_refresh(
        user.token, user.refresh_token, dt.datetime.fromisoformat(user.token_expires)
    )

    if new_auth_data["refreshed"]:
        user.load_auth_data_from_response(new_auth_data)
        user_repository.save_user(user)

    user_dict = asdict(user)
    for key in KEYS_TO_EXCLUDE_FROM_USER:
        del user_dict[key]

    return {"user": user_dict}


@bp.route("/<user_id>/session")
def user_session(user_id: str) -> ResponseReturnValue:
    try:
        session = user_repository.get_user_session(user_id)
    except InvalidJsonException:
        abort(400, f"User {user_id} data has an invalid format.")

    return {"session": _format_user_session(session)}


@bp.route("/<user_id>/session/<user_to_remove>", methods=["DELETE"])
def remove_user_from_session(user_id: str, user_to_remove: str) -> ResponseReturnValue:
    try:
        user_repository.remove_from_session(user_id, user_to_remove)
    except ValueError as e:
        abort(400, str(e))

    try:
        session = user_repository.get_user_session(user_id)
    except InvalidJsonException:
        abort(400, f"User {user_id} data has an invalid format.")

    return {"session": _format_user_session(session)}


def _format_user_session(session: list[SpotifyUser]) -> list[dict[str, str]] :
    session_dict: list[dict[str, str]] = []
    for user in session:
        user_dict = asdict(user)
        for key in KEYS_TO_EXCLUDE_FROM_USER:
            del user_dict[key]
        session_dict.append(user_dict)
    return session_dict
