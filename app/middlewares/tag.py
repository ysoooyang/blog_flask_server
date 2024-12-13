from functools import wraps
from flask import request, current_app
from app.utils.response import error_response, ErrorCode
from app.services.tag_service import TagService


def verify_tag(f):
    """验证标签参数"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            tag_name = data.get('tag_name')
            tag_id = data.get('id')

            if not tag_name:
                current_app.logger.error("标签名称不能为空")
                return error_response(ErrorCode.TAG, "标签名称不能为空")

            # 检查标签是否已存在
            existing_tag = TagService.get_one_tag({
                'tag_name': tag_name
            })

            if existing_tag and existing_tag.get('id') != tag_id:
                current_app.logger.error("标签已存在")
                return error_response(ErrorCode.TAG, "标签已存在")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"标签验证失败: {str(e)}")
            return error_response(ErrorCode.TAG, "标签验证失败")

    return decorated_function


def verify_delete_tags(f):
    """验证批量删除标签参数"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            tag_id_list = data.get('tagIdList', [])

            if not tag_id_list:
                current_app.logger.error("标签id列表不能为空")
                return error_response(ErrorCode.TAG, "标签id列表不能为空")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"标签删除验证失败: {str(e)}")
            return error_response(ErrorCode.TAG, "标签删除验证失败")

    return decorated_function