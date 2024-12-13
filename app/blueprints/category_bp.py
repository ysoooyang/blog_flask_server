from flask import Blueprint
from app.controllers.category_controller import bp as category_controller_bp

category_bp = Blueprint('category_bp', __name__)
category_bp.register_blueprint(category_controller_bp)