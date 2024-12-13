# app/models/message.py

from app.extensions.extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'blog_message'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(555), nullable=False, comment="留言内容")
    color = db.Column(db.String, default="#676767", comment="字体颜色")
    font_size = db.Column(db.Integer, default=12, comment="字体大小")
    font_weight = db.Column(db.Integer, default=500, comment="字体宽度")
    bg_color = db.Column(db.String, nullable=True, comment="背景颜色")
    bg_url = db.Column(db.String, nullable=True, comment="背景图片")
    user_id = db.Column(db.Integer, nullable=True, comment="留言用户的id")
    nick_name = db.Column(db.String, nullable=True, comment="游客用户的昵称")
    tag = db.Column(db.String, nullable=True, comment="标签")
    like_times = db.Column(db.Integer, default=0, comment="点赞次数")
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
            "color": self.color,
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "bg_color": self.bg_color,
            "bg_url": self.bg_url,
            "user_id": self.user_id,
            "nick_name": self.nick_name,
            "tag": self.tag,
            "like_times": self.like_times,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Message message={self.message}, user_id={self.user_id}>"