from flask import Blueprint
from app.controllers.comment_controller import bp as comment_controller_bp

comment_bp = Blueprint('comment_bp', __name__)
comment_bp.register_blueprint(comment_controller_bp)