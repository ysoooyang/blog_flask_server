from flask import Flask
from .user_bp import user_bp
from .utils_bp import utils_bp
from .article_bp import article_bp
from .category_bp import category_bp
from .category_bp_small import category_bp_small
from .chat_bp import chat_bp
from .comment_bp import comment_bp
from .config_bp import config_bp
from .header_bp import header_bp
from .like_bp import like_bp
from .links_bp import links_bp
from .message_bp import message_bp
from .notify_bp import notify_bp
from .photo_bp import photo_bp
from .photo_album_bp import photo_album_bp
from .statistic_bp import statistic_bp
from .tag_bp import tag_bp
from .talk_bp import talk_bp

def init_blueprints(app: Flask):
    """初始化所有蓝图"""
    # 注册用户蓝图
    app.register_blueprint(user_bp, url_prefix='/user')

    # 注册文章蓝图
    app.register_blueprint(article_bp, url_prefix='/article')

    # 注册分类蓝图
    app.register_blueprint(category_bp_small, url_prefix='/category')

    # 注册分类蓝图
    app.register_blueprint(category_bp, url_prefix='/Category')

    # 注册聊天蓝图
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # 注册评论蓝图
    app.register_blueprint(comment_bp, url_prefix='/comment')

    # 注册配置蓝图
    app.register_blueprint(config_bp, url_prefix='/config')

    # 注册头部背景蓝图
    app.register_blueprint(header_bp, url_prefix='/header')

    # 注册点赞蓝图
    app.register_blueprint(like_bp, url_prefix='/like')

    # 注册友链蓝图
    app.register_blueprint(links_bp, url_prefix='/links')

    # 注册留言蓝图
    app.register_blueprint(message_bp, url_prefix='/message')

    # 注册通知蓝图
    app.register_blueprint(notify_bp, url_prefix='/notify')

    # 注册照片蓝图
    app.register_blueprint(photo_bp, url_prefix='/photo')

    # 注册相册蓝图
    app.register_blueprint(photo_album_bp, url_prefix='/photoAlbum')

    # 注册统计蓝图
    app.register_blueprint(statistic_bp, url_prefix='/statistic')

    # 注册标签蓝图
    app.register_blueprint(tag_bp, url_prefix='/tag')

    # 注册说说蓝图
    app.register_blueprint(talk_bp, url_prefix='/talk')

    # 注册工具蓝图
    app.register_blueprint(utils_bp, url_prefix='/utils')