from flask import Blueprint
from app.controllers.like_controller import bp as like_controller_bp

like_bp = Blueprint('like_bp', __name__)
like_bp.register_blueprint(like_controller_bp)