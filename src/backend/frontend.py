from flask import Blueprint, current_app, redirect
from flask.typing import ResponseReturnValue

bp = Blueprint('frontend', __name__,  static_folder='../frontend')

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path: str) -> ResponseReturnValue:
    # TODO: if home, check first if user credentials are stored, so that they
    # don't need to click the login button and are instead logged in right away
    if current_app.debug:
        return redirect(f"http://{current_app.config['FRONTEND_SERVER_NAME']}")
    
    return bp.send_static_file("index.html")