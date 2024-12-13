from flask import Blueprint
from app.controllers.photo_album_controller import bp as photo_album_controller_bp

photo_album_bp = Blueprint('photo_album_bp', __name__)
photo_album_bp.register_blueprint(photo_album_controller_bp)