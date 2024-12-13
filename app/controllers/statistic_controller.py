from flask import Blueprint
from app.services.article_service import ArticleService
from app.services.tag_service import TagService
from app.services.category_service import CategoryService
from app.services.user_service import UserService
from app.utils.response import success_response, error_response

bp = Blueprint('statistic', __name__)


@bp.route('/', methods=['GET'])
def home_get_statistic():
    """获取首页统计数据"""
    try:
        article_count = ArticleService.get_article_count()
        tag_count = TagService.get_tag_count()
        category_count = CategoryService.get_category_count()
        user_count = UserService.get_user_count()

        data = {
            'articleCount': article_count,
            'tagCount': tag_count,
            'categoryCount': category_count,
            'userCount': user_count
        }

        return success_response("获取数据统计成功", data)
    except Exception as e:
        current_app.logger.error(f"获取数据统计失败: {str(e)}")
        return error_response("获取数据统计失败")