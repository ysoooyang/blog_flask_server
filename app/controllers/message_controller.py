from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.message_service import MessageService
from app.controllers.notify_controller import add_notify
from app.utils.response import success_response, error_response
from app.utils.sensitive import filter_sensitive
from app.utils.tool import random_nickname

bp = Blueprint('message', __name__)


@bp.route('', methods=['POST'])
def add_message():
    """发布留言"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        message = data.get('message')
        nick_name = data.get('nick_name')

        if not user_id:
            nick_name = random_nickname("游客", 5)

        message = filter_sensitive(message)
        res = MessageService.add_message(nick_name=nick_name, user_id=user_id, message=message, **data)

        if user_id != 1:
            add_notify({
                'user_id': 1,
                'type': 3,
                'message': f"您收到了来自于：{nick_name} 的留言: {message}！"
            })

        return success_response("发布成功", res)
    except Exception as e:
        current_app.logger.error(f"发布失败: {str(e)}")
        return error_response("发布失败")


@bp.route('', methods=['PUT'])
@jwt_required()
def update_message():
    """修改留言"""
    try:
        data = request.get_json()
        message = data.get('message')

        message = filter_sensitive(message)
        data['message'] = message
        res = MessageService.update_message(data)

        return success_response("修改成功", res)
    except Exception as e:
        current_app.logger.error(f"修改失败: {str(e)}")
        return error_response("修改失败")


@bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_message():
    """删除留言"""
    try:
        data = request.get_json()
        id_list = data.get('idList')
        res = MessageService.delete_message(id_list)
        return success_response("删除留言成功", res)
    except Exception as e:
        current_app.logger.error(f"删除留言失败: {str(e)}")
        return error_response("删除留言失败")


@bp.route('/<int:id>/like', methods=['PUT'])
def message_like(id):
    """留言点赞"""
    try:
        res = MessageService.message_like(id)
        return success_response("留言点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"留言点赞失败: {str(e)}")
        return error_response("留言点赞失败")


@bp.route('/<int:id>/cancel-like', methods=['PUT'])
def cancel_message_like(id):
    """取消留言点赞"""
    try:
        res = MessageService.cancel_message_like(id)
        return success_response("取消留言点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"取消留言点赞失败: {str(e)}")
        return error_response("取消留言点赞失败")


@bp.route('/list', methods=['POST'])
def get_message_list():
    """分页获取留言"""
    try:
        ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or request.remote_addr
        ip = ip.split(":")[-1]
        data = request.get_json()
        data['ip'] = ip
        res = MessageService.get_message_list(data)
        return success_response("分页获取留言成功", res)
    except Exception as e:
        current_app.logger.error(f"分页获取留言失败: {str(e)}")
        return error_response("分页获取留言失败")


@bp.route('/all', methods=['GET'])
def get_all_message():
    """获取所有留言"""
    try:
        res = MessageService.get_all_message()
        return success_response("获取留言成功", res)
    except Exception as e:
        current_app.logger.error(f"获取留言失败: {str(e)}")
        return error_response("获取留言失败")


@bp.route('/tags', methods=['GET'])
def get_message_tag():
    """获取热门标签"""
    try:
        res = MessageService.get_message_tag()
        return success_response("获取留言所有标签成功", res)
    except Exception as e:
        current_app.logger.error(f"获取留言所有标签失败: {str(e)}")
        return error_response("获取留言所有标签失败")