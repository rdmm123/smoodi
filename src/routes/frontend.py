from flask import Blueprint
from flask.typing import ResponseReturnValue

bp = Blueprint('frontend', __name__,  static_folder='../frontend')

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path: str) -> ResponseReturnValue:
    return bp.send_static_file("index.html")
