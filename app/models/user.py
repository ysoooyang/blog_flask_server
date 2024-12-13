# app/models/user.py

from app.extensions.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'blog_user'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False, comment="账号，唯一")
    password = db.Column(db.String(64), nullable=False, comment="密码")
    role = db.Column(db.Integer, nullable=False, default=2, comment="用户角色 1 管理员 2 普通用户")
    nick_name = db.Column(db.String(255), nullable=True, default="", comment="用户昵称")
    qq = db.Column(db.String(255), nullable=True, default="", comment="用户QQ 用于联系")
    ip = db.Column(db.String(255), nullable=True, default="", comment="IP属地")
    avatar = db.Column(db.String(255), nullable=True, default="", comment="用户头像")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, name="createdAt", comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, name="updatedAt",
                           comment="更新时间")

    # 自定义时间格式化方法
    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None

    # 转换为字典的方法
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,  # 请注意不要在实际返回中包含敏感信息
            "role": self.role,
            "nick_name": self.nick_name,
            "qq": self.qq,
            "ip": self.ip,
            "avatar": self.avatar,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<User username={self.username} role={self.role}>"