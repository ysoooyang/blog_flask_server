from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.tag_service import TagService
from app.utils.response import success_response, error_response
from app.middlewares import (
    verify_tag,
    verify_delete_tags,
    admin_required
)

bp = Blueprint('tag', __name__)

@bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@verify_tag
def add_tag():
    """新增标签"""
    try:
        data = request.get_json()
        res = TagService.create_tag(data)
        return success_response("新增标签成功", {
            'id': res['id'],
            'tag_name': res['tag_name']
        })
    except Exception as e:
        current_app.logger.error(f"新增标签失败: {str(e)}")
        return error_response("新增标签失败")

@bp.route('', methods=['PUT'])
@jwt_required()
@admin_required
@verify_tag
def update_tag():
    """修改标签"""
    try:
        data = request.get_json()
        res = TagService.update_tag(data)
        return success_response("修改标签成功", res)
    except Exception as e:
        current_app.logger.error(f"修改标签失败: {str(e)}")
        return error_response("修改标签失败")

@bp.route('/delete', methods=['POST'])
@jwt_required()
@admin_required
@verify_delete_tags
def delete_tags():
    """删除标签"""
    try:
        data = request.get_json()
        tag_id_list = data.get('tagIdList')
        res = TagService.delete_tags(tag_id_list)
        return success_response("删除标签成功", {
            'updateNum': res
        })
    except Exception as e:
        current_app.logger.error(f"删除标签失败: {str(e)}")
        return error_response("删除标签失败")

@bp.route('/getTagList', methods=['POST'])
def get_tag_list():
    """分页查找标签"""
    try:
        data = request.get_json()
        res = TagService.get_tag_list(data)
        return success_response("分页查找标签成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找标签失败: {str(e)}")
        return error_response("分页查找标签失败")

@bp.route('/getTagDictionary', methods=['GET'])
def get_tag_dictionary():
    """获取标签字典"""
    try:
        res = TagService.get_tag_dictionary()
        return success_response("获取标签字典成功", res)
    except Exception as e:
        current_app.logger.error(f"获取标签字典失败: {str(e)}")
        return error_response("获取标签字典失败")