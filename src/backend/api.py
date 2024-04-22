from flask import Blueprint, session, current_app

bp = Blueprint('api', __name__, url_prefix='/api')
@bp.route('/current_user')
def current_user():
    current_user = session.get('email')
    return {
        'current_user': current_user
    }