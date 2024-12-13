from flask import Blueprint
from app.controllers.chat_controller import bp as chat_controller_bp

chat_bp = Blueprint('chat_bp', __name__)
chat_bp.register_blueprint(chat_controller_bp)