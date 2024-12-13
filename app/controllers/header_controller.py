from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.header_service import HeaderService
from app.utils.response import success_response, error_response
from app.utils.qiniu_upload import delete_imgs

bp = Blueprint('header', __name__)


@bp.route('', methods=['POST'])
@jwt_required()
def add_or_update_header():
    """新增/修改背景图"""
    try:
        data = request.get_json()
        id = data.get('id')
        route_name = data.get('route_name')

        # 检查路径是否存在
        existing_header = HeaderService.get_one_by_path(route_name)
        if not id and existing_header:
            return error_response("已经存在相同的背景路径")
        if id and existing_header and existing_header['id'] != id:
            return error_response("已经存在相同的背景路径")

        res = HeaderService.add_or_update_header(data)
        msg = "修改" if id else "新增"
        return success_response(f"{msg}背景成功", res)
    except Exception as e:
        current_app.logger.error(f"背景操作失败: {str(e)}")
        return error_response(f"{msg}背景失败")


@bp.route('', methods=['DELETE'])
@jwt_required()
def delete_header():
    """删除背景图"""
    try:
        data = request.get_json()
        id = data.get('id')
        url = data.get('url')

        res = HeaderService.delete_header(id)

        if url:
            filename = url.split("/")[-1]
            delete_imgs([filename])

        return success_response("删除背景成功", res)
    except Exception as e:
        current_app.logger.error(f"删除背景失败: {str(e)}")
        return error_response("删除背景失败")


@bp.route('', methods=['GET'])
def get_all_header():
    """获取所有背景图"""
    try:
        res = HeaderService.get_all_header()
        return success_response("获取所有背景成功", res)
    except Exception as e:
        current_app.logger.error(f"获取所有背景失败: {str(e)}")
        return error_response("获取所有背景失败")