from flask import Blueprint
from app.controllers.config_controller import bp as config_controller_bp

config_bp = Blueprint('config_bp', __name__)
config_bp.register_blueprint(config_controller_bp)