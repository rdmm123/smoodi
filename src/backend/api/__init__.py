from flask import Blueprint
from backend.api import users, blender

bp = Blueprint('api', __name__, url_prefix='/api')
bp.register_blueprint(users.bp)
bp.register_blueprint(blender.bp)