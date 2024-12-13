from flask import Blueprint
from app.controllers.statistic_controller import bp as statistic_controller_bp

statistic_bp = Blueprint('statistic_bp', __name__)
statistic_bp.register_blueprint(statistic_controller_bp)