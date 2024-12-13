# app/models/header.py

from app.extensions.extensions import db
from datetime import datetime

class Header(db.Model):
    __tablename__ = 'blog_header'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name = db.Column(db.String(555), nullable=False, comment="路由名称")
    bg_url = db.Column(db.String, nullable=False, comment="背景图")
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
            "route_name": self.route_name,
            "bg_url": self.bg_url,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Header route_name={self.route_name}>"