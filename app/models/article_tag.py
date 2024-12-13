# app/models/article_tag.py.py

from app.extensions.extensions import db  # 引入 db
from datetime import datetime

class ArticleTag(db.Model):
    __tablename__ = 'blog_article_tag'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 自动生成的主键
    article_id = db.Column(db.Integer, nullable=False, comment="文章id")
    tag_id = db.Column(db.Integer, nullable=False, comment="标签id")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 自定义返回时间格式
    @property
    def formatted_created_at(self):
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None

    @property
    def formatted_updated_at(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None

    # to_dict 方法
    def to_dict(self):
        return {
            "id": self.id,
            "article_id": self.article_id,
            "tag_id": self.tag_id,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at
        }

    def __repr__(self):
        return f"<ArticleTag article_id={self.article_id}, tag_id={self.tag_id}>"