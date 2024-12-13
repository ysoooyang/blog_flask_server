from flask import Blueprint
from app.controllers.talk_controller import bp as talk_controller_bp

talk_bp = Blueprint('talk_bp', __name__)
talk_bp.register_blueprint(talk_controller_bp)