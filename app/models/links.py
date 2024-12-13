# app/models/links.py

from app.extensions.extensions import db
from datetime import datetime

class Links(db.Model):
    __tablename__ = 'blog_links'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_name = db.Column(db.String(55), nullable=False, comment="网站名称")
    site_desc = db.Column(db.String, nullable=True, comment="网站描述")
    site_avatar = db.Column(db.String(555), nullable=True, comment="网站头像")
    url = db.Column(db.String, nullable=False, comment="网站地址")
    status = db.Column(db.Integer, nullable=False, comment="友链状态 1 待审核 2 审核通过")
    user_id = db.Column(db.String, nullable=False, comment="申请者id")
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
            "site_name": self.site_name,
            "site_desc": self.site_desc,
            "site_avatar": self.site_avatar,
            "url": self.url,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Links site_name={self.site_name}, url={self.url}>"