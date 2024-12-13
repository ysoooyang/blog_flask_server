import bcrypt
from flask import Blueprint
from flask import request, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.services.user_service import UserService
from app.utils.response import success_response, error_response, ErrorCode
from app.utils.tool import get_ip_address
from app.utils.upload import delete_images
from app.middlewares import (
    admin_required,
    super_admin_forbidden,
    user_validate,
    verify_user,
    crypt_password,
    verify_login,
    verify_update_password,
)

bp = Blueprint('user', __name__)


@bp.route('/register', methods=['POST'])
@user_validate
@verify_user
@crypt_password
def register():
    """用户注册"""
    try:
        user_data = request.get_json()
        user = UserService.create_user(user_data)

        if not user:
            return error_response(ErrorCode.USER, "用户注册失败")

        # 保存用户IP
        ip = request.headers.get('X-Real-IP') or \
             request.headers.get('X-Forwarded-For') or \
             request.remote_addr
        UserService.update_ip(user['id'], ip.split(':')[-1])

        return success_response(
            message="用户注册成功",
            data={
                'id': user['id'],
                'username': user['username']
            }
        )

    except Exception as e:
        current_app.logger.error(f"用户注册失败: {str(e)}")
        return error_response(ErrorCode.USER, "用户注册失败")


@bp.route('/login', methods=['POST'])
@user_validate
@verify_login
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 超级管理员登录
        if username == 'admin':
            if password == current_app.config['ADMIN_PASSWORD']:
                token = create_access_token(identity={
                    'nick_name': '超级管理员',
                    'id': 5201314,
                    'role': 1,
                    'username': 'admin'
                })
                return success_response("超级管理员登录成功", {
                    'token': token,
                    'username': '超级管理员',
                    'role': 1,
                    'id': 5201314
                })
            return error_response(ErrorCode.USER, "密码错误")

        # 普通用户登录
        user = UserService.get_one_user_info(username=username)
        if not user:
            return error_response(ErrorCode.USER, "用户不存在")

        # 验证密码
        if not bcrypt.checkpw(password.encode(), user['password'].encode()):
            return error_response(ErrorCode.USER, "密码错误")

        # 更新IP
        ip = request.headers.get('X-Real-IP') or \
             request.headers.get('X-Forwarded-For') or \
             request.remote_addr
        UserService.update_ip(user['id'], ip.split(':')[-1])

        # 生成token
        user_data = {k: v for k, v in user.items() if k != 'password'}
        token = create_access_token(identity=user_data)

        return success_response("用户登录成功", {
            'token': token,
            'username': user['username'],
            'role': user['role'],
            'id': user['id']
        })

    except Exception as e:
        current_app.logger.error(f"用户登录失败: {str(e)}")
        return error_response(ErrorCode.USER, "用户登录失败")


@bp.route('/getUserInfoById/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_info(user_id):
    """获取用户信息"""
    try:
        if user_id == 5201314:
            return success_response("获取用户信息成功", {
                'id': 5201314,
                'role': 1,
                'nick_name': '超级管理员'
            })

        user = UserService.get_one_user_info(user_id=user_id)
        if not user:
            return error_response(ErrorCode.USER, "用户不存在")

        # 移除敏感信息
        user_info = {k: v for k, v in user.items()
                     if k not in ['password', 'username', 'ip']}
        user_info['ip_address'] = get_ip_address(user.get('ip', ''))

        return success_response("获取用户信息成功", user_info)

    except Exception as e:
        current_app.logger.error(f"获取用户信息失败: {str(e)}")
        return error_response(ErrorCode.USER, "获取用户信息失败")


@bp.route('/update', methods=['PUT'])
@jwt_required()
@super_admin_forbidden  # 超级管理员不能修改自己的信息
def update_own_user_info():
    """更新用户信息"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['id']
        data = request.get_json()

        # 处理头像更新
        if 'avatar' in data:
            old_user = UserService.get_one_user_info(user_id=user_id)
            if old_user and old_user['avatar'] != data['avatar']:
                delete_images([old_user['avatar']])

        success = UserService.update_own_user_info(user_id, data)
        if not success:
            return error_response(ErrorCode.USER, "更新用户信息失败")

        return success_response("更新用户信息成功")

    except Exception as e:
        current_app.logger.error(f"更新用户信息失败: {str(e)}")
        return error_response(ErrorCode.USER, "更新用户信息失败")


@bp.route('/password', methods=['PUT'])
@jwt_required()
@super_admin_forbidden  # 超级管理员不能修改密码
@verify_update_password
def update_password():
    """修改密码"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user['id']

        if user_id == 2:
            return error_response(ErrorCode.USER, "测试用户密码不可以修改哦")

        data = request.get_json()
        password = data.get('password1')

        success = UserService.update_password(user_id, password)
        if not success:
            return error_response(ErrorCode.USER, "修改密码失败")

        return success_response("修改密码成功")

    except Exception as e:
        current_app.logger.error(f"修改密码失败: {str(e)}")
        return error_response(ErrorCode.USER, "修改密码失败")


@bp.route('/role/<int:user_id>/<int:role>', methods=['PUT'])
@jwt_required()
@admin_required  # 需要管理员权限
def update_role(user_id, role):
    """修改用户角色"""
    try:
        success = UserService.update_role(user_id, role)
        if not success:
            return error_response(ErrorCode.USER, "修改角色失败")

        return success_response("修改角色成功")

    except Exception as e:
        current_app.logger.error(f"修改角色失败: {str(e)}")
        return error_response(ErrorCode.USER, "修改角色失败")


@bp.route('/getUserList', methods=['POST'])
@jwt_required()
@admin_required  # 需要管理员权限
def get_user_list():
    """获取用户列表"""
    try:
        data = request.get_json()
        current = data.get('current', 1)
        size = data.get('size', 10)
        nick_name = data.get('nick_name')
        role = data.get('role')

        result = UserService.get_user_list(current, size, nick_name, role)
        return success_response("获取用户列表成功", result)

    except Exception as e:
        current_app.logger.error(f"获取用户列表失败: {str(e)}")
        return error_response(ErrorCode.USER, "获取用户列表失败")


@bp.route('/admin/update', methods=['PUT'])
@jwt_required()
@admin_required  # 需要管理员权限
@super_admin_forbidden  # 超级管理员不能修改用户信息
def admin_update_user_info():
    """管理员更新用户信息"""
    try:
        data = request.get_json()
        user_id = data.get('id')

        # 处理头像更新
        if 'avatar' in data:
            old_user = UserService.get_one_user_info(user_id=user_id)
            if old_user and old_user['avatar'] != data['avatar']:
                delete_images([old_user['avatar']])

        success = UserService.admin_update_user_info(data)
        if not success:
            return error_response(ErrorCode.USER, "更新用户信息失败")

        return success_response("更新用户信息成功")

    except Exception as e:
        current_app.logger.error(f"更新用户信息失败: {str(e)}")
        return error_response(ErrorCode.USER, "更新用户信息失败")
