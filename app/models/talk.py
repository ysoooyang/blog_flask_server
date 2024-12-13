# app/models/talk.py

from app.extensions.extensions import db
from datetime import datetime

class Talk(db.Model):
    __tablename__ = 'blog_talk'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False, comment="说说内容")
    user_id = db.Column(db.Integer, nullable=False, comment="发布说说的用户id")
    status = db.Column(db.Integer, nullable=False, default=1, comment="说说状态 1 公开 2 私密 3 回收站")
    is_top = db.Column(db.Integer, nullable=False, default=2, comment="是否置顶 1 置顶 2 不置顶")
    like_times = db.Column(db.Integer, default=0, comment="点赞次数")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, name="createdAt", comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, name="updatedAt", onupdate=datetime.utcnow, comment="更新时间")

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
            "content": self.content,
            "user_id": self.user_id,
            "status": self.status,
            "is_top": self.is_top,
            "like_times": self.like_times,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Talk content={self.content[:20]} user_id={self.user_id}>"