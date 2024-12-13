from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.notify_service import NotifyService
from app.utils.response import success_response, error_response

bp = Blueprint('notify', __name__)

def add_notify(data):
    """新增消息通知"""
    try:
        NotifyService.create_notify(data)
    except Exception as e:
        current_app.logger.error(f"新增消息通知失败: {str(e)}")

@bp.route('/<int:id>/read', methods=['PUT'])
@jwt_required()
def update_notify(id):
    """已阅消息通知"""
    try:
        res = NotifyService.update_notify(id)
        return success_response("已阅消息通知成功", res)
    except Exception as e:
        current_app.logger.error(f"已阅消息通知失败: {str(e)}")
        return error_response("已阅消息通知失败")

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_notifys(id):
    """删除消息通知"""
    try:
        res = NotifyService.delete_notifys(id)
        return success_response("删除消息通知成功", {'res': res})
    except Exception as e:
        current_app.logger.error(f"删除消息通知失败: {str(e)}")
        return error_response("删除消息通知失败")

@bp.route('/list', methods=['POST'])
@jwt_required()
def get_notify_list():
    """分页查找消息通知"""
    try:
        data = request.get_json()
        res = NotifyService.get_notify_list(data)
        return success_response("分页查找消息通知成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查询消息通知失败: {str(e)}")
        return error_response("分页查询消息通知失败")