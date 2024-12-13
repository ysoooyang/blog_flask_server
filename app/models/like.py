# app/models/like.py

from app.extensions.extensions import db
from datetime import datetime

class Like(db.Model):
    __tablename__ = 'blog_like'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False, comment="点赞类型 1 文章 2 说说 3 留言 4 评论")
    for_id = db.Column(db.Integer, nullable=False, comment="点赞的id 文章id 说说id 留言id")
    user_id = db.Column(db.Integer, nullable=True, comment="点赞用户id")
    ip = db.Column(db.String, nullable=False, comment="点赞ip")
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
            "type": self.type,
            "for_id": self.for_id,
            "user_id": self.user_id,
            "ip": self.ip,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Like for_id={self.for_id}, user_id={self.user_id}>"