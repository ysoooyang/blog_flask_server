from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.category_service import CategoryService
from app.utils.response import success_response, error_response
from app.middlewares import (
    verify_category,
    verify_delete_categories,
    admin_required
)

bp = Blueprint('Category', __name__)

bp_small = Blueprint('category', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
@admin_required
@verify_category
def add_category():
    """新增分类"""
    try:
        data = request.get_json()
        res = CategoryService.create_category(data)
        return success_response("新增分类成功", {
            'id': res.id,
            'category_name': res.category_name
        })
    except Exception as e:
        current_app.logger.error(f"新增分类失败: {str(e)}")
        return error_response("新增分类失败")

@bp.route('/', methods=['PUT'])
@jwt_required()
@admin_required
@verify_category
def update_category():
    """修改分类"""
    try:
        data = request.get_json()
        res = CategoryService.update_category(data)
        return success_response("修改分类成功", res)
    except Exception as e:
        current_app.logger.error(f"修改分类失败: {str(e)}")
        return error_response("修改分类失败")

@bp.route('/delete', methods=['POST'])
@jwt_required()
@admin_required
@verify_delete_categories
def delete_categories():
    """删除分类"""
    try:
        category_id_list = request.json.get('categoryIdList')
        res = CategoryService.delete_categories(category_id_list)
        return success_response("删除分类成功", {
            'updateNum': res
        })
    except Exception as e:
        current_app.logger.error(f"删除分类失败: {str(e)}")
        return error_response("删除分类失败")

@bp.route('/getCategoryList', methods=['POST'])
@bp_small.route('/getCategoryList', methods=['POST'])
@jwt_required()
def get_category_list():
    """条件分页查找分类列表"""
    try:
        data = request.get_json()
        current = data.get('current')
        size = data.get('size')
        category_name = data.get('category_name')
        res = CategoryService.get_category_list(current, size, category_name)
        return success_response("分页查找分类成功", res)
    except Exception as e:
        current_app.logger.error(f"分页查找分类失败: {str(e)}")
        return error_response("分页查找分类失败")

@bp.route('/getCategoryDictionary', methods=['GET'])
@jwt_required()
def get_category_dictionary():
    """获取分类字典"""
    try:
        res = CategoryService.get_category_dictionary()
        return success_response("获取分类字典成功", res)
    except Exception as e:
        current_app.logger.error(f"获取分类字典失败: {str(e)}")
        return error_response("获取分类字典失败")