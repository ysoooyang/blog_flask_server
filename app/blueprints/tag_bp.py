from flask import Blueprint
from app.controllers.tag_controller import bp as tag_controller_bp

tag_bp = Blueprint('tag_bp', __name__)
tag_bp.register_blueprint(tag_controller_bp)