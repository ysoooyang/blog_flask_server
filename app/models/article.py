# app/models/article.py

from app.extensions.extensions import db  # 引入 db
from datetime import datetime

class Article(db.Model):
    __tablename__ = 'blog_article'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_title = db.Column(db.String, nullable=False, comment="文章标题 不能为空")
    author_id = db.Column(db.Integer, nullable=False, default=1, comment="文章作者 不能为空")
    category_id = db.Column(db.Integer, nullable=False, comment="分类id 不能为空")
    article_description = db.Column(db.String, nullable=False, comment="描述信息 不能为空")
    article_content = db.Column(db.Text, nullable=False, comment="文章内容")
    article_cover = db.Column(db.String(1234), nullable=True, default="https://mrzym.gitee.io/blogimg/html/rabbit.png", comment="文章缩略图")
    is_top = db.Column(db.Integer, nullable=False, default=2, comment="是否置顶 1 置顶 2 取消置顶")
    order = db.Column(db.Integer, nullable=True, comment="排序 1 最大 往后越小 用于置顶文章的排序")
    status = db.Column(db.Integer, nullable=False, default=1, comment="文章状态  1 公开 2 私密 3 草稿箱")
    type = db.Column(db.Integer, nullable=False, default=1, comment="文章类型 1 原创 2 转载 3 翻译")
    origin_url = db.Column(db.String, nullable=True, comment="原文链接 是转载或翻译的情况下提供")
    view_times = db.Column(db.Integer, nullable=False, default=0, comment="文章访问次数")
    thumbs_up_times = db.Column(db.Integer, nullable=False, default=0, comment="文章点赞次数")
    reading_duration = db.Column(db.Float, nullable=True, default=0.0, comment="文章阅读时长")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 自定义返回时间格式
    @property
    def formatted_created_at(self):
        """格式化创建时间"""
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None

    @property
    def formatted_updated_at(self):
        """格式化更新时间"""
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None

    def to_dict(self):
        """将对象序列化为字典"""
        return {
            'id': self.id,
            'article_title': self.article_title,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'article_description': self.article_description,
            'article_content': self.article_content,
            'article_cover': self.article_cover,
            'is_top': self.is_top,
            'order': self.order,
            'status': self.status,
            'type': self.type,
            'origin_url': self.origin_url,
            'view_times': self.view_times,
            'thumbs_up_times': self.thumbs_up_times,
            'reading_duration': self.reading_duration,
            'created_at': self.formatted_created_at,
            'updated_at': self.formatted_updated_at,
        }

    def __repr__(self):
        """打印对象信息"""
        return f"<Article {self.article_title}>"