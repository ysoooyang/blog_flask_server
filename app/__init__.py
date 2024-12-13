from flask import Flask
from .middlewares.limit_request import create_limiter
from .config.config import Config
from .extensions.extensions import db, migrate, jwt, cors, limiter
from .extensions import init_extensions
from .blueprints import init_blueprints


def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    init_extensions(app)

    # 初始化限流器
    limiter = create_limiter(app)

    # 初始化上传文件夹
    Config.init_upload_folder()

    # 初始化所有扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    # 注册蓝图
    init_blueprints(app)

    return app