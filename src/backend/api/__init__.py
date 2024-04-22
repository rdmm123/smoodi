from flask import Blueprint
from backend.api import users

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(users.bp)