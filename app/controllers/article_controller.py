from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.article_service import ArticleService
from app.services.article_tag_service import ArticleTagService
from app.utils.response import success_response, error_response, ErrorCode
from app.utils.article_common import create_category_or_return, create_article_tag_by_article_id
from app.middlewares import (
    verify_article_param,
    create_judge_title_exist,
    update_judge_title_exist,
    verify_top_param,
    verify_del_param
)

bp = Blueprint('article', __name__)


@bp.route('/', methods=['POST'])
@jwt_required()
@verify_article_param
@create_judge_title_exist
def create_article():
    """新增文章"""
    try:
        data = request.get_json()
        tag_list = data.pop('tagList', [])
        category = data.pop('category', {})

        # 处理分类
        data['category_id'] = create_category_or_return(
            category.get('id'),
            category.get('category_name')
        )

        # 创建文章
        new_article = ArticleService.create_article(data)
        if not new_article:
            return error_response(ErrorCode.ARTICLE, "新增文章失败")

        # 处理标签关联
        new_article_tag_list = create_article_tag_by_article_id(
            new_article['id'],
            tag_list
        )

        return success_response("新增文章成功", {
            'article': new_article,
            'articleTagList': new_article_tag_list
        })
    except Exception as e:
        current_app.logger.error(f"新增文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "新增文章失败")


@bp.route('', methods=['PUT'])
@jwt_required()
@verify_article_param
@update_judge_title_exist
def update_article():
    """修改文章"""
    try:
        data = request.get_json()
        tag_list = data.pop('tagList', [])
        category = data.pop('category', {})

        # 处理分类
        data['category_id'] = create_category_or_return(
            category.get('id'),
            category.get('category_name')
        )

        # 删除旧的标签关联
        ArticleTagService.delete_article_tag(data.get('id'))

        # 更新文章
        success = ArticleService.update_article(data)
        if not success:
            return error_response(ErrorCode.ARTICLE, "修改文章失败")

        # 处理新的标签关联
        new_article_tag_list = create_article_tag_by_article_id(
            data.get('id'),
            tag_list
        )

        return success_response("修改文章成功", {
            'res': success,
            'newArticleTagList': new_article_tag_list
        })
    except Exception as e:
        current_app.logger.error(f"修改文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "修改文章失败")


@bp.route('/<int:id>/top/<int:is_top>', methods=['PUT'])
@jwt_required()
@verify_top_param
def update_top(id, is_top):
    """修改文章置顶状态"""
    try:
        success = ArticleService.update_top(id, is_top)
        if not success:
            return error_response(ErrorCode.ARTICLE, "修改文章置顶状态失败")

        return success_response("修改文章置顶状态成功", success)
    except Exception as e:
        current_app.logger.error(f"修改文章置顶状态失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "修改文章置顶状态失败")


@bp.route('/<int:id>/<int:status>', methods=['DELETE'])
@jwt_required()
@verify_del_param
def delete_article(id, status):
    """删除文章"""
    try:
        success = ArticleService.delete_article(id, status)
        if not success:
            return error_response(ErrorCode.ARTICLE, "删除文章失败")

        return success_response("删除文章成功", success)
    except Exception as e:
        current_app.logger.error(f"删除文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "删除文章失败")


@bp.route('/<int:id>/revert', methods=['PUT'])
@jwt_required()
def revert_article(id):
    """恢复文章"""
    try:
        success = ArticleService.revert_article(id)
        if not success:
            return error_response(ErrorCode.ARTICLE, "恢复文章失败")

        return success_response("恢复文章成功", success)
    except Exception as e:
        current_app.logger.error(f"恢复文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "恢复文章失败")


@bp.route('/<int:id>/public/<int:status>', methods=['PUT'])
@jwt_required()
def toggle_article_public(id, status):
    """公开或隐藏文章"""
    try:
        success = ArticleService.toggle_article_public(id, status)
        if not success:
            return error_response(ErrorCode.ARTICLE, "公开或隐藏文章失败")

        message = "公开文章" if status == 1 else "隐藏文章"
        return success_response(f"{message}成功", success)
    except Exception as e:
        current_app.logger.error(f"公开或隐藏文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "公开或隐藏文章失败")


@bp.route('/blogHomeGetArticleList', methods=['POST'])
@jwt_required()
def get_article_list():
    """条件分页获取文章"""
    try:
        params = request.get_json()
        result = ArticleService.get_article_list(params)
        return success_response("查询文章成功", result)
    except Exception as e:
        current_app.logger.error(f"查询文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "查询文章失败")


@bp.route('/title', methods=['POST'])
@jwt_required()
def get_article_info_by_title():
    """根据标题获取文章是否已经存在"""
    try:
        data = request.get_json()
        id = data.get('id')
        article_title = data.get('article_title')
        exists = ArticleService.get_article_info_by_title(id, article_title)
        return success_response("文章查询结果", exists)
    except Exception as e:
        current_app.logger.error(f"根据标题查询文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "根据标题查询文章失败")


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_article_by_id(id):
    """根据id获取文章信息"""
    try:
        article = ArticleService.get_article_by_id(id)
        return success_response("查询文章详情成功", article)
    except Exception as e:
        current_app.logger.error(f"查询文章详情失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "查询文章详情失败")


@bp.route('/recommend/<int:id>', methods=['GET'])
@jwt_required()
def get_recommend_article_by_id(id):
    """根据文章获取上下一篇文章 和推荐文章"""
    try:
        result = ArticleService.get_recommend_article_by_id(id)
        return success_response("获取推荐文章成功", result)
    except Exception as e:
        current_app.logger.error(f"获取推荐文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "获取推荐文章失败")


@bp.route('/content', methods=['POST'])
@jwt_required()
def get_article_list_by_content():
    """全局搜索文章"""
    try:
        content = request.json.get('content')
        result = ArticleService.get_article_list_by_content(content)
        return success_response("按照内容搜索文章成功", result)
    except Exception as e:
        current_app.logger.error(f"按照内容搜索文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "按照内容搜索文章失败")


@bp.route('/hot', methods=['GET'])
@jwt_required()
def get_hot_article():
    """获取热门文章"""
    try:
        result = ArticleService.get_hot_article()
        return success_response("获取热门文章成功", result)
    except Exception as e:
        current_app.logger.error(f"获取热门文章失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "获取热门文章失败")


@bp.route('/<int:id>/like', methods=['POST'])
@jwt_required()
def article_like(id):
    """文章点赞"""
    try:
        success = ArticleService.article_like(id)
        if not success:
            return error_response(ErrorCode.ARTICLE, "点赞失败")

        return success_response("点赞成功", success)
    except Exception as e:
        current_app.logger.error(f"点赞失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "点赞失败")


@bp.route('/<int:id>/like', methods=['DELETE'])
@jwt_required()
def cancel_article_like(id):
    """取消文章点赞"""
    try:
        success = ArticleService.cancel_article_like(id)
        if not success:
            return error_response(ErrorCode.ARTICLE, "取消点赞失败")

        return success_response("取消点赞成功", success)
    except Exception as e:
        current_app.logger.error(f"取消点赞失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "取消点赞失败")


@bp.route('/<int:id>/duration', methods=['POST'])
@jwt_required()
def add_reading_duration(id):
    """增加阅读时长"""
    try:
        duration = request.json.get('duration')
        success = ArticleService.add_reading_duration(id, duration)
        if not success:
            return error_response(ErrorCode.ARTICLE, "增加阅读时长失败")

        return success_response("增加阅读时长成功", success)
    except Exception as e:
        current_app.logger.error(f"增加阅读时长失败: {str(e)}")
        return error_response(ErrorCode.ARTICLE, "增加阅读时长失败")