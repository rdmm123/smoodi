import json
import traceback
from flask import current_app

from flask.typing import ResponseReturnValue

from werkzeug.exceptions import HTTPException

from src.core.client.base import InvalidResponseException, InvalidStatusException


def handle_invalid_api_response(e: InvalidResponseException) -> ResponseReturnValue:
    return {"message": str(e)}, 400


def handle_invalid_api_status(e: InvalidStatusException) -> ResponseReturnValue:
    return {"message": str(e)}, e.status_code


def handle_http_exception(e: HTTPException) -> ResponseReturnValue:
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()

    # replace the body with JSON
    response.data = json.dumps(  # type: ignore
        {
            "message": e.description,
        }
    )
    response.content_type = "application/json"
    return response


def handle_general_exception(e: Exception) -> ResponseReturnValue:
    current_app.logger.error(f"Uncaught exception: \n{traceback.format_exc()}")
    return {"message": "Internal server error"}, 500
