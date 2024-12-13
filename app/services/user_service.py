from typing import Optional, Dict
import bcrypt
from flask import current_app
from app.extensions.extensions import db
from app.models import User
from app.utils.sensitive import filter_sensitive
from app.utils.tool import random_nickname, get_ip_address


class UserService:
    @staticmethod
    def create_user(user_data: Dict) -> Optional[Dict]:
        """创建用户"""
        try:
            username = user_data.get('username')
            password = user_data.get('password')
            nick_name = user_data.get('nick_name')
            qq = user_data.get('qq')

            # 过滤敏感词
            nick_name = filter_sensitive(nick_name)
            # 随机生成昵称
            nick_name = nick_name or random_nickname("小张的迷弟")

            user = User(
                username=username,
                password=password,
                nick_name=nick_name,
                qq=qq,
                avatar="http://mrzym.top/online/9bb507f4bd065759a3d093d04.webp",
                role=2
            )

            db.session.add(user)
            db.session.commit()

            return user.to_dict()

        except Exception as e:
            current_app.logger.error(f"创建用户失败: {str(e)}")
            db.session.rollback()
            return None

    @staticmethod
    def update_own_user_info(user_id: int, user_data: Dict) -> bool:
        """更新用户信息"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            avatar = user_data.get('avatar')
            nick_name = user_data.get('nick_name')
            qq = user_data.get('qq')

            nick_name = filter_sensitive(nick_name)

            user.avatar = avatar
            user.nick_name = nick_name
            user.qq = qq

            db.session.commit()
            return True

        except Exception as e:
            current_app.logger.error(f"更新用户信息失败: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def update_password(user_id: int, password: str) -> bool:
        """修改用户密码"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            user.password = hashed_password.decode()

            db.session.commit()
            return True

        except Exception as e:
            current_app.logger.error(f"修改密码失败: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def update_role(user_id: int, role: int) -> bool:
        """修改用户角色"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            user.role = role
            db.session.commit()
            return True

        except Exception as e:
            current_app.logger.error(f"修改角色失败: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def get_one_user_info(user_id: int = None, username: str = None,
                          password: str = None, role: int = None) -> Optional[Dict]:
        """获取单个用户信息"""
        try:
            query = User.query

            if user_id:
                query = query.filter(User.id == user_id)
            if username:
                query = query.filter(User.username == username)
            if password:
                query = query.filter(User.password == password)
            if role:
                query = query.filter(User.role == role)

            user = query.first()
            return user.to_dict() if user else None

        except Exception as e:
            current_app.logger.error(f"获取用户信息失败: {str(e)}")
            return None

    @staticmethod
    def get_user_list(current: int, size: int, nick_name: str = None,
                      role: int = None) -> Dict:
        """分页获取用户列表"""
        try:
            query = User.query

            if role is not None:
                query = query.filter(User.role == role)
            if nick_name:
                query = query.filter(User.nick_name.like(f'%{nick_name}%'))

            total = query.count()
            users = query.offset((current - 1) * size).limit(size).all()

            user_list = []
            for user in users:
                user_dict = user.to_dict()
                if user.ip:
                    user_dict['ip_address'] = get_ip_address(user.ip)
                else:
                    user_dict['ip_address'] = "火星"
                user_list.append(user_dict)

            return {
                'current': current,
                'size': size,
                'total': total,
                'list': user_list
            }

        except Exception as e:
            current_app.logger.error(f"获取用户列表失败: {str(e)}")
            return {
                'current': current,
                'size': size,
                'total': 0,
                'list': []
            }

    @staticmethod
    def update_ip(user_id: int, ip: str) -> bool:
        """更新用户IP"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            user.ip = ip
            db.session.commit()
            return True

        except Exception as e:
            current_app.logger.error(f"更新IP失败: {str(e)}")
            db.session.rollback()
            return False

    @staticmethod
    def get_author_name_by_id(user_id: int) -> Optional[str]:
        """根据ID获取用户昵称"""
        try:
            user = User.query.get(user_id)
            return user.nick_name if user else None

        except Exception as e:
            current_app.logger.error(f"获取用户昵称失败: {str(e)}")
            return None

    @staticmethod
    def get_user_count() -> int:
        """获取用户总数"""
        try:
            return User.query.count()
        except Exception as e:
            current_app.logger.error(f"获取用户总数失败: {str(e)}")
            return 0

    @staticmethod
    def admin_update_user_info(user_data: Dict) -> bool:
        """管理员更新用户信息"""
        try:
            user_id = user_data.get('id')
            user = User.query.get(user_id)
            if not user:
                return False

            user.nick_name = user_data.get('nick_name', user.nick_name)
            user.avatar = user_data.get('avatar', user.avatar)

            db.session.commit()
            return True

        except Exception as e:
            current_app.logger.error(f"管理员更新用户信息失败: {str(e)}")
            db.session.rollback()
            return False
