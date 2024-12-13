# app/models/comment.py

from app.extensions.extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'blog_comment'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, nullable=True, comment="评论父级id")
    type = db.Column(db.Integer, nullable=True, comment="评论类型 1 文章 2 说说 3 留言 ...")
    for_id = db.Column(db.Integer, nullable=True, comment="评论的对象id 比如说说id、文章id等")
    from_id = db.Column(db.Integer, nullable=True, comment="评论人id")
    from_name = db.Column(db.String, nullable=True, comment="评论人昵称")
    from_avatar = db.Column(db.String(555), nullable=True, comment="评论人头像")
    to_id = db.Column(db.Integer, nullable=True, comment="被回复的人id")
    to_name = db.Column(db.String, nullable=True, comment="被回复人的昵称")
    to_avatar = db.Column(db.String(555), nullable=True, comment="被回复人的头像")
    content = db.Column(db.String(555), nullable=False, comment="评论内容")
    thumbs_up = db.Column(db.Integer, nullable=True, default=0, comment="评论点赞数")
    ip = db.Column(db.String, nullable=True, comment="ip地址")
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
            "parent_id": self.parent_id,
            "type": self.type,
            "for_id": self.for_id,
            "from_id": self.from_id,
            "from_name": self.from_name,
            "from_avatar": self.from_avatar,
            "to_id": self.to_id,
            "to_name": self.to_name,
            "to_avatar": self.to_avatar,
            "content": self.content,
            "thumbs_up": self.thumbs_up,
            "ip": self.ip,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Comment from_id={self.from_id}, content={self.content}>"