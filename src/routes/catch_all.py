from flask import Blueprint

bp = Blueprint('catch_all', __name__,  static_folder='../frontend')

@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def catch_all(path):
    return bp.send_static_file("index.html")
