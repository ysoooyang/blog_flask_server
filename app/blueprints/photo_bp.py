from flask import Blueprint
from app.controllers.photo_controller import bp as photo_controller_bp

photo_bp = Blueprint('photo_bp', __name__)
photo_bp.register_blueprint(photo_controller_bp)