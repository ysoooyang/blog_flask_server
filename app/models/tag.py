# app/models/tag.py

from app.extensions.extensions import db
from datetime import datetime

class Tag(db.Model):
    __tablename__ = 'blog_tag'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(55), nullable=False, unique=True, comment="标签名称 唯一")
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
            "tag_name": self.tag_name,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Tag tag_name={self.tag_name}>"