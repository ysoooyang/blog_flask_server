# app/models/chat.py

from app.extensions.extensions import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'blog_chat'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, comment="用户id 用于判断是谁发送的")
    content = db.Column(db.String(555), nullable=False, comment="聊天内容")
    content_type = db.Column(db.String(55), nullable=False, comment="聊天的内容格式 如果是文本就是text 图片就是 img")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 自定义返回时间格式
    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None

    # 转换为字典方法
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "content_type": self.content_type,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Chat user_id={self.user_id}, content={self.content}>"