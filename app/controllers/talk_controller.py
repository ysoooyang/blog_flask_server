from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.talk_service import TalkService
from app.utils.response import success_response, error_response

bp = Blueprint('talk', __name__)


@bp.route('publishTalk', methods=['POST'])
@jwt_required()
def publish_talk():
    """发布说说"""
    try:
        data = request.get_json()
        res = TalkService.publish_talk(data)
        return success_response("发布说说成功", {'id': res['id']})
    except Exception as e:
        current_app.logger.error(f"发布说说失败: {str(e)}")
        return error_response("发布说说失败")


@bp.route('', methods=['PUT'])
@jwt_required()
def update_talk():
    """修改说说"""
    try:
        data = request.get_json()
        res = TalkService.update_talk(data)
        return success_response("修改说说成功", res)
    except Exception as e:
        current_app.logger.error(f"修改说说失败: {str(e)}")
        return error_response("修改说说失败")


@bp.route('/<int:id>/<int:status>', methods=['DELETE'])
@jwt_required()
def delete_talk_by_id(id, status):
    """删除说说"""
    try:
        message = "删除" if status == 3 else "回收"
        res = TalkService.delete_talk_by_id(id, status)
        return success_response(f"{message}说说成功", res)
    except Exception as e:
        current_app.logger.error(f"{message}说说失败: {str(e)}")
        return error_response(f"{message}说说失败")


@bp.route('/<int:id>/public/<int:status>', methods=['PUT'])
@jwt_required()
def toggle_public(id, status):
    """公开/私密说说"""
    try:
        message = "公开" if status == 1 else "私密"
        res = TalkService.toggle_public(id, status)
        return success_response(f"{message}说说成功", res)
    except Exception as e:
        current_app.logger.error(f"{message}说说失败: {str(e)}")
        return error_response(f"{message}说说失败")


@bp.route('/<int:id>/like', methods=['PUT'])
def talk_like(id):
    """说说点赞"""
    try:
        res = TalkService.talk_like(id)
        return success_response("点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"点赞失败: {str(e)}")
        return error_response("点赞失败")


@bp.route('/<int:id>/like/cancel', methods=['PUT'])
def cancel_talk_like(id):
    """取消说说点赞"""
    try:
        res = TalkService.cancel_talk_like(id)
        return success_response("取消点赞成功", res)
    except Exception as e:
        current_app.logger.error(f"取消点赞失败: {str(e)}")
        return error_response("取消点赞失败")


@bp.route('/<int:id>/revert', methods=['PUT'])
@jwt_required()
def revert_talk(id):
    """恢复说说"""
    try:
        res = TalkService.revert_talk(id)
        return success_response("恢复说说成功", res)
    except Exception as e:
        current_app.logger.error(f"恢复说说失败: {str(e)}")
        return error_response("恢复说说失败")


@bp.route('/<int:id>/top/<int:is_top>', methods=['PUT'])
@jwt_required()
def toggle_top(id, is_top):
    """切换置顶状态"""
    try:
        message = "置顶" if is_top == 1 else "取消置顶"
        res = TalkService.toggle_top(id, is_top)
        return success_response(f"{message}说说成功", res)
    except Exception as e:
        current_app.logger.error(f"{message}说说失败: {str(e)}")
        return error_response(f"{message}说说失败")


@bp.route('/getTalkList', methods=['POST'])
def get_talk_list():
    """分页获取说说"""
    try:
        data = request.get_json()
        res = TalkService.get_talk_list(
            data.get('current'),
            data.get('size'),
            data.get('status')
        )
        return success_response("获取说说列表成功", res)
    except Exception as e:
        current_app.logger.error(f"获取说说列表失败: {str(e)}")
        return error_response("获取说说列表失败")


@bp.route('/<int:id>', methods=['GET'])
def get_talk_by_id(id):
    """根据id获取说说详情"""
    try:
        res = TalkService.get_talk_by_id(id)
        return success_response("获取说说详情成功", res)
    except Exception as e:
        current_app.logger.error(f"获取说说详情失败: {str(e)}")
        return error_response("获取说说详情失败")


@bp.route('/blog/list', methods=['POST'])
def blog_get_talk_list():
    """前台获取说说列表"""
    try:
        data = request.get_json()
        ip = request.headers.get('X-Real-IP') or \
             request.headers.get('X-Forwarded-For') or \
             request.remote_addr
        ip = ip.split(":")[-1]

        res = TalkService.blog_get_talk_list(
            data.get('current'),
            data.get('size'),
            data.get('user_id'),
            ip
        )
        return success_response("获取说说列表成功", res)
    except Exception as e:
        current_app.logger.error(f"获取说说列表失败: {str(e)}")
        return error_response("获取说说列表失败")