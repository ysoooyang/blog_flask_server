from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.chat_service import ChatService
from app.utils.response import success_response, error_response
from app.utils.qiniu_upload import delete_imgs

bp = Blueprint('chat', __name__)

@bp.route('', methods=['POST'])
@jwt_required()
def create_chat():
    """新增聊天"""
    try:
        data = request.get_json()
        res = ChatService.create_chat(data)
        return success_response("新增聊天成功", {'content': res.content})
    except Exception as e:
        current_app.logger.error(f"新增聊天失败: {str(e)}")
        return error_response("新增聊天失败")

@bp.route('', methods=['DELETE'])
@jwt_required()
def delete_chats():
    """删除聊天"""
    try:
        # 寻找所有的聊天记录 依次删除图片
        chats = ChatService.get_all_chats()
        if chats:
            filenames = [chat.content.split("/")[-1] for chat in chats]
            delete_imgs(filenames)

        ChatService.delete_chats()
        return success_response("删除聊天成功")
    except Exception as e:
        current_app.logger.error(f"删除聊天失败: {str(e)}")
        return error_response("删除聊天失败")

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_chat(id):
    """删除单条聊天记录"""
    try:
        chat = ChatService.get_one_chat(id)
        if chat.content_type == "image":
            filename = chat.content.split("/")[-1]
            delete_imgs([filename])

        ChatService.delete_one_chat(id)
        return success_response("撤回聊天成功")
    except Exception as e:
        current_app.logger.error(f"撤回聊天失败: {str(e)}")
        return error_response("撤回聊天失败")

@bp.route('/getChatList', methods=['POST'])
@jwt_required()
def get_chat_list():
    """条件分页查找聊天列表"""
    try:
        data = request.get_json()
        res = ChatService.get_chat_list(data)
        return success_response("分页查找聊天成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找聊天失败: {str(e)}")
        return error_response("分页查找聊天失败")