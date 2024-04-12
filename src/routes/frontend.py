from flask import Blueprint
from flask.typing import ResponseReturnValue

bp = Blueprint('frontend', __name__,  static_folder='../frontend')

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path: str) -> ResponseReturnValue:
    # TODO: if home, check first if user credentials are stored, so that they
    # don't need to click the login button and are instead logged in right away
    return bp.send_static_file("index.html")
