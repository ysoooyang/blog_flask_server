# app/models/talk_photo.py

from app.extensions.extensions import db
from datetime import datetime

class TalkPhoto(db.Model):
    __tablename__ = 'blog_talk_photo'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    talk_id = db.Column(db.Integer, nullable=False, comment="说说的id")
    url = db.Column(db.String(255), nullable=False, comment="图片地址")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

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
            "talk_id": self.talk_id,
            "url": self.url,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<TalkPhoto talk_id={self.talk_id} url={self.url}>"