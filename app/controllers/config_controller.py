from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from app.services.config_service import ConfigService
from app.utils.response import success_response, error_response

bp = Blueprint('config', __name__)

@bp.route('', methods=['PUT'])
@jwt_required()
def update_config():
    """更新配置"""
    try:
        data = request.get_json()
        res = ConfigService.update_config(data)
        return success_response("更新配置成功" if res else "更新配置失败")
    except Exception as e:
        current_app.logger.error(f"更新配置失败: {str(e)}")
        return error_response("更新配置失败")

@bp.route('/', methods=['GET'])
def get_config():
    """获取配置"""
    try:
        config = ConfigService.get_config()
        return success_response("获取配置成功", config.to_dict() if config else None)
    except Exception as e:
        current_app.logger.error(f"获取配置失败: {str(e)}")
        return error_response("获取配置失败")

@bp.route('/view', methods=['POST'])
def add_view():
    """增加访问量"""
    try:
        result = ConfigService.add_view()
        return success_response("增加访问量成功", {'message': result})
    except Exception as e:
        current_app.logger.error(f"增加访问量失败: {str(e)}")
        return error_response("增加访问量失败")