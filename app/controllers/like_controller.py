from flask import Blueprint, request, current_app
from app.services.like_service import LikeService
from app.services.article_service import ArticleService
from app.services.talk_service import TalkService
from app.services.message_service import MessageService
from app.services.comment_service import CommentService
from app.utils.response import success_response, error_response

bp = Blueprint('like', __name__)


@bp.route('', methods=['POST'])
def add_like():
    """点赞"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        ip = ip.split(":")[-1]
        data = request.get_json()
        for_id = data.get('for_id')
        type_ = data.get('type')
        user_id = data.get('user_id')

        if not for_id:
            return error_response("点赞对象不能为空")
        if not type_:
            return error_response("点赞类型不能为空")

        if not user_id:
            is_like = LikeService.get_is_like_by_ip_and_type(for_id, type_, ip)
            if is_like:
                return error_response("您已经点过赞了")
            res = LikeService.add_like(for_id=for_id, type_=type_, ip=ip)
        else:
            is_like = LikeService.get_is_like_by_id_and_type(for_id, type_, user_id)
            if is_like:
                return error_response("您已经点过赞了")
            res = LikeService.add_like(for_id=for_id, type_=type_, user_id=user_id)

        if not res:
            return error_response("点赞失败")

        # 处理不同类型的点赞
        type_handlers = {
            "1": ArticleService.article_like,
            "2": TalkService.talk_like,
            "3": MessageService.message_like,
            "4": CommentService.comment_like
        }

        if str(type_) in type_handlers:
            type_handlers[str(type_)](for_id)

        return success_response("点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"点赞失败: {str(e)}")
        return error_response("点赞失败")


@bp.route('/cancel', methods=['POST'])
def cancel_like():
    """取消点赞"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        ip = ip.split(":")[-1]
        data = request.get_json()
        for_id = data.get('for_id')
        type_ = data.get('type')
        user_id = data.get('user_id')

        if not for_id:
            return error_response("取消点赞对象不能为空")
        if not type_:
            return error_response("取消点赞类型不能为空")

        if not user_id:
            is_like = LikeService.get_is_like_by_ip_and_type(for_id, type_, ip)
            if not is_like:
                return error_response("您没有点过赞")
            res = LikeService.cancel_like(for_id=for_id, type_=type_, ip=ip)
        else:
            is_like = LikeService.get_is_like_by_id_and_type(for_id, type_, user_id)
            if not is_like:
                return error_response("您没有点过赞")
            res = LikeService.cancel_like(for_id=for_id, type_=type_, user_id=user_id)

        if not res:
            return error_response("取消点赞失败")

        # 处理不同类型的取消点赞
        type_handlers = {
            "1": ArticleService.cancel_article_like,
            "2": TalkService.cancel_talk_like,
            "3": MessageService.cancel_message_like,
            "4": CommentService.cancel_comment_like
        }

        if str(type_) in type_handlers:
            type_handlers[str(type_)](for_id)

        return success_response("取消点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"取消点赞失败: {str(e)}")
        return error_response("取消点赞失败")


@bp.route('/status', methods=['POST'])
def get_is_like_by_id_or_ip_and_type():
    """获取点赞状态"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        ip = ip.split(":")[-1]
        data = request.get_json()
        for_id = data.get('for_id')
        type_ = data.get('type')
        user_id = data.get('user_id')

        if not for_id:
            return error_response("点赞对象不能为空")
        if not type_:
            return error_response("点赞类型不能为空")

        if not user_id:
            res = LikeService.get_is_like_by_ip_and_type(for_id, type_, ip)
        else:
            res = LikeService.get_is_like_by_id_and_type(for_id, type_, user_id)

        return success_response("获取用户是否点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"获取用户是否点赞失败: {str(e)}")
        return error_response("获取用户是否点赞失败")