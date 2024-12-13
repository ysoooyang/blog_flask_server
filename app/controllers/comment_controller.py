from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.comment_service import CommentService
from app.utils.response import success_response, error_response
from app.controllers.notify_controller import add_notify
from app.utils.tool import get_current_type_name
from app.utils.sensitive import filter_sensitive
from app.middlewares import create_times_limiter

bp = Blueprint('comment', __name__)

@bp.route('', methods=['POST'])
@jwt_required()
@create_times_limiter(
    prefix_key="like",
    interval=30,
    max_requests=3,
    message="评论太频繁了，休息一下吧"
)
def add_comment():
    """新增评论"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        data = request.get_json()
        data['content'] = filter_sensitive(data['content'])
        data['ip'] = ip.split(":")[-1]

        res = CommentService.create_comment(data)
        if data['from_id'] != data['author_id']:
            add_notify({
                'user_id': data['author_id'],
                'type': data['type'],
                'to_id': data['for_id'],
                'message': f"您的{get_current_type_name(data['type'])}收到了来自于：{data['from_name']} 的评论: {data['content']}！"
            })

        return success_response("新增评论成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"新增评论失败: {str(e)}")
        return error_response("新增评论失败")

@bp.route('/reply', methods=['POST'])
@jwt_required()
@create_times_limiter(
    prefix_key="like",
    interval=30,
    max_requests=3,
    message="回复太频繁了，休息一下吧"
)
def apply_comment():
    """回复评论"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        data = request.get_json()
        data['content'] = filter_sensitive(data['content'])
        data['ip'] = ip.split(":")[-1]

        res = CommentService.apply_comment(data)
        if data['from_id'] != data['to_id']:
            add_notify({
                'user_id': data['to_id'],
                'type': data['type'],
                'to_id': data['for_id'],
                'message': f"您的收到了来自于：{data['from_name']} 的评论回复: {data['content']}！"
            })

        return success_response("回复评论成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"回复评论失败: {str(e)}")
        return error_response("回复评论失败")

@bp.route('/<int:id>/like', methods=['POST'])
@jwt_required()
@create_times_limiter(
    prefix_key="like",
    interval=30,
    max_requests=3,
    message="点赞太频繁了，休息一下吧"
)
def comment_like(id):
    """点赞评论"""
    try:
        res = CommentService.comment_like(id)
        return success_response("点赞成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"点赞失败: {str(e)}")
        return error_response("点赞失败")

@bp.route('/<int:id>/like', methods=['DELETE'])
@jwt_required()
def cancel_comment_like(id):
    """取消点赞评论"""
    try:
        res = CommentService.cancel_comment_like(id)
        return success_response("取消点赞成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"取消点赞失败: {str(e)}")
        return error_response("取消点赞失败")

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):
    """删除评论"""
    try:
        parent_id = request.args.get('parent_id', type=int)
        res = CommentService.delete_comment(id, parent_id)
        return success_response("删除评论成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"删除评论失败: {str(e)}")
        return error_response("删除评论失败")

@bp.route('/list', methods=['POST'])
@jwt_required()
def back_get_comment_list():
    """后台条件分页查找评论列表"""
    try:
        data = request.get_json()
        res = CommentService.back_get_comment_list(data)
        return success_response("分页查找评论成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找评论失败: {str(e)}")
        return error_response("分页查找评论失败")

@bp.route('/parent', methods=['POST'])
@jwt_required()
def front_get_parent_comment():
    """前台条件分页查找父级评论列表"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        data = request.get_json()
        data['ip'] = ip.split(":")[-1]
        res = CommentService.front_get_parent_comment(data)
        return success_response("分页查找评论成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找评论失败: {str(e)}")
        return error_response("分页查找评论失败")

@bp.route('/children', methods=['POST'])
@jwt_required()
def front_get_children_comment():
    """前台条件分页查找子级评论列表"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        data = request.get_json()
        data['ip'] = ip.split(":")[-1]
        res = CommentService.front_get_children_comment(data)
        return success_response("分页查找子评论成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找子评论失败: {str(e)}")
        return error_response("分页查找子评论失败")

@bp.route('/total', methods=['POST'])
@jwt_required()
def get_comment_total():
    """获取当前评论的总条数"""
    try:
        data = request.get_json()
        res = CommentService.get_comment_total(data)
        return success_response("获取评论总条数成功", res)
    except Exception as e:
        current_app.logger.error(f"获取评论总条数失败: {str(e)}")
        return error_response("获取评论总条数失败")