from flask import Blueprint
from app.controllers.links_controller import bp as links_controller_bp

links_bp = Blueprint('links_bp', __name__)
links_bp.register_blueprint(links_controller_bp)