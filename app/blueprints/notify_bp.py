from flask import Blueprint
from app.controllers.notify_controller import bp as notify_controller_bp

notify_bp = Blueprint('notify_bp', __name__)
notify_bp.register_blueprint(notify_controller_bp)