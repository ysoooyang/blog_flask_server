# app/models/config.py

from app.extensions.extensions import db
from datetime import datetime

class Config(db.Model):
    __tablename__ = 'blog_config'  # 表名
    __table_args__ = {'extend_existing': True}  # 防止表重复定义

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog_name = db.Column(db.String(55), nullable=False, default="小张的博客", comment="博客名称")
    blog_avatar = db.Column(db.String, nullable=False, default="https://mrzym.gitee.io/blogimg/html/rabbit.png", comment="博客头像")
    avatar_bg = db.Column(db.String, nullable=False, comment="博客头像背景图")
    personal_say = db.Column(db.String, nullable=False, comment="个人签名")
    blog_notice = db.Column(db.String, nullable=True, comment="博客公告")
    qq_link = db.Column(db.String, nullable=False, comment="qq链接")
    we_chat_link = db.Column(db.String, nullable=False, comment="微信链接")
    github_link = db.Column(db.String, nullable=False, comment="github链接")
    git_ee_link = db.Column(db.String, nullable=False, comment="git_ee链接")
    bilibili_link = db.Column(db.String, nullable=False, comment="bilibili链接")
    view_time = db.Column(db.BigInteger, nullable=False, default=0, comment="博客被访问的次数")
    we_chat_group = db.Column(db.String, nullable=True, comment="微信群图片")
    qq_group = db.Column(db.String, nullable=True, comment="qq群图片")
    we_chat_pay = db.Column(db.String, nullable=True, comment="微信收款码")
    ali_pay = db.Column(db.String, nullable=True, comment="支付宝收款码")
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
            "blog_name": self.blog_name,
            "blog_avatar": self.blog_avatar,
            "avatar_bg": self.avatar_bg,
            "personal_say": self.personal_say,
            "blog_notice": self.blog_notice,
            "qq_link": self.qq_link,
            "we_chat_link": self.we_chat_link,
            "github_link": self.github_link,
            "git_ee_link": self.git_ee_link,
            "bilibili_link": self.bilibili_link,
            "view_time": self.view_time,
            "we_chat_group": self.we_chat_group,
            "qq_group": self.qq_group,
            "we_chat_pay": self.we_chat_pay,
            "ali_pay": self.ali_pay,
            "created_at": self.formatted_created_at,
            "updated_at": self.formatted_updated_at,
        }

    def __repr__(self):
        return f"<Config blog_name={self.blog_name}>"