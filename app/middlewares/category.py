from functools import wraps
from flask import request, current_app
from app.utils.response import error_response, ErrorCode
from app.services.category_service import CategoryService


def verify_category(f):
    """验证分类参数"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            category_name = data.get('category_name')
            category_id = data.get('id')

            if not category_name:
                current_app.logger.error("分类名称不能为空")
                return error_response(ErrorCode.CATEGORY, "分类名称不能为空")

            # 检查分类是否已存在
            existing_category = CategoryService.get_one_category({
                'category_name': category_name
            })

            if existing_category and existing_category.get('id') == category_id:
                current_app.logger.error("分类已存在")
                return error_response(ErrorCode.CATEGORY, "分类已存在")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"分类验证失败: {str(e)}")
            return error_response(ErrorCode.CATEGORY, "分类验证失败")

    return decorated_function


def verify_delete_categories(f):
    """验证批量删除分类参数"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            category_id_list = data.get('categoryIdList', [])

            if not category_id_list:
                current_app.logger.error("分类id列表不能为空")
                return error_response(ErrorCode.CATEGORY, "分类id列表不能为空")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"分类删除验证失败: {str(e)}")
            return error_response(ErrorCode.CATEGORY, "分类删除验证失败")

    return decorated_function