from flask import Blueprint
from app.controllers.category_controller import bp as category_controller_bp

category_bp_small = Blueprint('category_bp_small', __name__)
category_bp_small.register_blueprint(category_controller_bp)