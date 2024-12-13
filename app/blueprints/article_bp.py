from flask import Blueprint
from app.controllers.article_controller import bp as article_controller_bp

article_bp = Blueprint('article_bp', __name__)

# 注册文章控制器的路由
article_bp.register_blueprint(article_controller_bp)