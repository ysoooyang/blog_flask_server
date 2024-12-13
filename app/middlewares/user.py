from functools import wraps
import bcrypt
import re
from flask import request, current_app
from flask_jwt_extended import get_jwt_identity
from app.utils.response import error_response, ErrorCode
from app.services.user_service import UserService


def user_validate(f):
    """校验用户名和密码是否合法"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            # 检查是否为空
            if not username or not password:
                current_app.logger.error("用户名或密码为空")
                return error_response(ErrorCode.USER, "用户名或密码为空")

            # 检查用户名格式
            if not re.match(r'^[A-Za-z0-9]+$', username):
                current_app.logger.error("用户名只能是数字和字母组成")
                return error_response(ErrorCode.USER, "用户名只能是数字和字母组成")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"用户参数验证失败: {str(e)}")
            return error_response(ErrorCode.USER, "用户参数验证失败")

    return decorated_function


def verify_user(f):
    """校验用户名是否已经注册过"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            username = data.get('username')

            if username == 'admin':
                current_app.logger.error("admin账号已存在")
                return error_response(ErrorCode.USER, "admin账号已存在")

            existing_user = UserService.get_one_user_info(username=username)
            if existing_user:
                current_app.logger.error("用户名已经存在")
                return error_response(ErrorCode.USER, "用户名已经存在")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"用户验证失败: {str(e)}")
            return error_response(ErrorCode.USER, "用户获取信息错误")

    return decorated_function


def crypt_password(f):
    """生成加盐的密码"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            password = data.get('password')

            # 生成加盐密码
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode(), salt)
            data['password'] = hashed.decode()

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"密码加密失败: {str(e)}")
            return error_response(ErrorCode.USER, "密码加密失败")

    return decorated_function


def verify_login(f):
    """判断用户名和密码匹配"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if username != 'admin':
                user = UserService.get_one_user_info(username=username)

                if not user:
                    current_app.logger.error("用户名不存在")
                    return error_response(ErrorCode.USER, "用户名不存在")

                if not bcrypt.checkpw(
                        password.encode(),
                        user['password'].encode()
                ):
                    current_app.logger.error("密码不匹配")
                    return error_response(ErrorCode.USER, "密码不匹配")

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"登录验证失败: {str(e)}")
            return error_response(ErrorCode.USER, "用户校验失败")

    return decorated_function


def verify_update_password(f):
    """验证修改密码"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            current_user = get_jwt_identity()
            username = current_user.get('username')

            if username != 'admin':
                data = request.get_json()
                password = data.get('password')
                password1 = data.get('password1')
                password2 = data.get('password2')

                if password1 != password2:
                    current_app.logger.error("两次输入密码不一致")
                    return error_response(ErrorCode.USER, "两次输入密码不一致")

                user = UserService.get_one_user_info(username=username)
                if not bcrypt.checkpw(
                        password.encode(),
                        user['password'].encode()
                ):
                    current_app.logger.error("密码不匹配")
                    return error_response(ErrorCode.USER, "密码不匹配")
            else:
                return error_response(
                    ErrorCode.USER,
                    "admin密码只可以通过配置文件env修改"
                )

            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"修改密码验证失败: {str(e)}")
            return error_response(ErrorCode.USER, "修改密码校验失败")

    return decorated_function