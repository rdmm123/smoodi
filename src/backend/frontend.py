from flask import Blueprint, current_app, redirect, request
from flask.typing import ResponseReturnValue

bp = Blueprint('frontend', __name__,  static_folder='../frontend/dist')

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path: str) -> ResponseReturnValue:
    if current_app.config['ENV'] == 'development':
        return redirect(f"http://{current_app.config['FRONTEND_SERVER_NAME']}"
                        f"/{path}?{request.query_string.decode()}")
    
    return bp.send_static_file("index.html")
