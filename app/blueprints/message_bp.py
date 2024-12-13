from flask import Blueprint
from app.controllers.message_controller import bp as message_controller_bp

message_bp = Blueprint('message_bp', __name__)
message_bp.register_blueprint(message_controller_bp)