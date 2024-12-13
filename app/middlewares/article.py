from functools import wraps
from flask import request, current_app
from app.utils.response import throw_error,ErrorCode
from app.services.article_service import ArticleService

def verify_article_param(f):
    """新增/编辑文章校验参数"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        article_title = data.get('article_title')
        author_id = data.get('author_id')
        category = data.get('category')
        article_content = data.get('article_content')
        tag_list = data.get('tagList', [])

        if not category:
            current_app.logger.error("文章分类必传")
            return throw_error(ErrorCode.ARTICLE, "文章分类必传")

        category_name = category.get('category_name')

        if not all([article_title, author_id, category_name, article_content]):
            current_app.logger.error("文章参数校验错误")
            return throw_error("文章参数校验错误", ErrorCode.ARTICLE)

        if not tag_list:
            return throw_error("文章标签不能为空", ErrorCode.ARTICLE)

        return f(*args, **kwargs)

    return decorated_function


def create_judge_title_exist(f):
    """新增文章判断标题是否已经存在过"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        article_title = data.get('article_title')

        res = ArticleService.get_article_info_by_title({'article_title': article_title})
        if res:
            return throw_error("已存在相同的文章标题", ErrorCode.ARTICLE)

        return f(*args, **kwargs)

    return decorated_function


def update_judge_title_exist(f):
    """编辑文章判断被修改的标题是否已经存在"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        article_id = data.get('id')
        article_title = data.get('article_title')

        res = ArticleService.get_article_info_by_title({
            'id': article_id,
            'article_title': article_title
        })
        if res:
            return throw_error("已存在相同的文章标题", ErrorCode.ARTICLE)

        return f(*args, **kwargs)

    return decorated_function


def verify_top_param(f):
    """验证置顶参数"""

    @wraps(f)
    def decorated_function(id, is_top, *args, **kwargs):
        if not (str(id).isdigit() and str(is_top).isdigit()):
            return throw_error("参数只能为数字", ErrorCode.ARTICLE)

        return f(id, is_top, *args, **kwargs)

    return decorated_function


def verify_del_param(f):
    """验证删除参数"""

    @wraps(f)
    def decorated_function(id, status, *args, **kwargs):
        if not (str(id).isdigit() and str(status).isdigit()):
            return throw_error("参数只能为数字", ErrorCode.ARTICLE)

        return f(id, status, *args, **kwargs)

    return decorated_function