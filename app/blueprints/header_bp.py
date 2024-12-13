from flask import Blueprint
from app.controllers.header_controller import bp as header_controller_bp

header_bp = Blueprint('header_bp', __name__)
header_bp.register_blueprint(header_controller_bp)