from functools import wraps

from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.utils.response import error_response, ErrorCode


def auth_required(f):
    """基础认证中间件"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            error_type = str(e)
            if 'ExpiredSignatureError' in error_type:
                current_app.logger.error("token已过期")
                return error_response(ErrorCode.AUTHTOKEN, "token已过期")
            else:
                current_app.logger.error("无效的token")
                return error_response(ErrorCode.AUTH, "无效的token")

    return decorated_function


def admin_required_not_super(f):
    """需要管理员权限但不建议超级管理员使用的接口"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if current_user.get('role') != 1:
                current_app.logger.error("普通用户仅限查看")
                return error_response(ErrorCode.AUTH, "普通用户仅限查看")

            if current_user.get('username') == 'admin':
                current_app.logger.error("admin是配置的用户，没有用户信息，建议注册账号再发布博客内容")
                return error_response(
                    ErrorCode.AUTH,
                    "admin是配置的用户，没有用户信息，建议注册账号再发布博客内容"
                )

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"认证失败: {str(e)}")
            return error_response(ErrorCode.AUTH, "认证失败")

    return decorated_function


def admin_required(f):
    """需要管理员权限的接口"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if current_user.get('role') != 1:
                current_app.logger.error("普通用户仅限查看")
                return error_response(ErrorCode.AUTH, "普通用户仅限查看")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"认证失败: {str(e)}")
            return error_response(ErrorCode.AUTH, "认证失败")

    return decorated_function


def super_admin_forbidden(f):
    """禁止超级管理员访问的接口"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user = get_jwt_identity()

            if current_user.get('username') == 'admin':
                current_app.logger.error("管理员信息只可通过配置信息修改")
                return error_response(ErrorCode.AUTH, "管理员信息只可通过配置信息修改")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"认证失败: {str(e)}")
            return error_response(ErrorCode.AUTH, "认证失败")

    return decorated_function