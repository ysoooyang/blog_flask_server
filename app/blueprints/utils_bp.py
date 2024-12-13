from flask import Blueprint
from app.controllers.utils_controller import bp as utils_controller_bp

utils_bp = Blueprint('utils_bp', __name__)
utils_bp.register_blueprint(utils_controller_bp)