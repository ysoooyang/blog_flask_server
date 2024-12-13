# app/models/notify.py

from app.extensions.extensions import db
from datetime import datetime

class Notify(db.Model):
    __tablename__ = 'blog_notify'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(555), nullable=False, comment="通知内容")
    user_id = db.Column(db.Integer, nullable=False, comment="通知给谁")
    type = db.Column(db.Integer, nullable=False, comment="通知类型 1 文章 2 说说 3 留言 4 友链")
    to_id = db.Column(db.Integer, nullable=True, comment="说说或者是文章的id，用于跳转")
    is_view = db.Column(db.Integer, default=1, nullable=False, comment="是否被查看 1 没有 2 已经查看")
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
            "message": self.message,
            "user_id": self.user_id,
            "type": self.type,
            "to_id": self.to_id,
            "is_view": self.is_view,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Notify message={self.message}, user_id={self.user_id}, type={self.type}>"