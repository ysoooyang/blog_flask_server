from flask import Blueprint
from app.controllers.user_controller import bp as user_controller_bp

user_bp = Blueprint('user_bp', __name__)
user_bp.register_blueprint(user_controller_bp)

