from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.links_service import LinksService
from app.controllers.notify_controller import add_notify
from app.utils.response import success_response, error_response

bp = Blueprint('links', __name__)


@bp.route('', methods=['POST'])
@jwt_required()
def add_or_update_links():
    """新增/修改友链"""
    try:
        data = request.get_json()
        id = data.get('id')
        site_name = data.get('site_name')

        res = LinksService.add_or_update_links(data)
        if not id:
            add_notify({
                'user_id': 1,
                'type': 4,  # 友链
                'message': f"您的收到了来自于：{site_name} 的友链申请，点我去后台审核！"
            })

        msg = "修改" if id else "发布"
        return success_response(f"{msg}友链成功", res)
    except Exception as e:
        current_app.logger.error(f"友链操作失败: {str(e)}")
        return error_response(f"{msg}友链失败")


@bp.route('/front', methods=['POST'])
@jwt_required()
def front_update_links():
    """博客前台 修改友链"""
    try:
        data = request.get_json()
        site_name = data.get('site_name')

        res = LinksService.add_or_update_links(data)
        add_notify({
            'user_id': 1,
            'type': 4,  # 友链
            'message': f"您的收到了来自于：{site_name} 的友链修改申请，点我去后台审核！"
        })

        return success_response("修改友链成功", res)
    except Exception as e:
        current_app.logger.error(f"修改友链失败: {str(e)}")
        return error_response("修改友链失败")


@bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_links():
    """批量删除友链"""
    try:
        data = request.get_json()
        id_list = data.get('idList')

        res = LinksService.delete_links(id_list)
        return success_response("删除友链成功", res)
    except Exception as e:
        current_app.logger.error(f"删除友链失败: {str(e)}")
        return error_response("删除友链失败")


@bp.route('/approve', methods=['POST'])
@jwt_required()
def approve_links():
    """审核友链"""
    try:
        data = request.get_json()
        id_list = data.get('idList')

        res = LinksService.approve_links(id_list)
        return success_response("审核友链成功", res)
    except Exception as e:
        current_app.logger.error(f"审核友链失败: {str(e)}")
        return error_response("审核友链失败")


@bp.route('/list', methods=['POST'])
def get_links_list():
    """分页获取友链"""
    try:
        data = request.get_json()
        res = LinksService.get_links_list(data)
        return success_response("查询友链成功", res)
    except Exception as e:
        current_app.logger.error(f"查询友链失败: {str(e)}")
        return error_response("查询友链失败")