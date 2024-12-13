import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()


class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')

    # JWT配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # Token过期时间
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # 刷新Token过期时间
    JWT_ERROR_MESSAGE_KEY = 'message'  # JWT错误消息的键名

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = bool(int(os.getenv('SQLALCHEMY_ECHO', '0')))  # SQL语句输出

    # 数据库连接池配置
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', '5'))  # 连接池大小
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', '10'))  # 连接超时
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '300'))  # 连接回收时间
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '10'))  # 最大溢出连接数

    # 文件上传配置
    UPLOAD_TYPE = os.getenv('UPLOAD_TYPE', 'local')  # local/qiniu/minio/online
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', '16 * 1024 * 1024'))  # 最大16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # 七牛云配置
    QINIU_ACCESS_KEY = os.getenv('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.getenv('QINIU_SECRET_KEY')
    QINIU_BUCKET = os.getenv('QINIU_BUCKET')
    QINIU_DOMAIN = os.getenv('QINIU_DOMAIN')  # 七牛云域名

    # MinIO配置
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET')
    MINIO_PATH = os.getenv('MINIO_PATH', 'localhost')
    MINIO_PORT = int(os.getenv('MINIO_PORT', '9000'))
    MINIO_SECURE = bool(int(os.getenv('MINIO_SECURE', '0')))  # 是否使用HTTPS

    # 管理员配置
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

    # 跨域配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']

    # 限流配置
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '200 per day, 50 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_upload_folder():
        """初始化上传文件夹"""
        folders = [
            Config.UPLOAD_FOLDER,
            os.path.join(Config.UPLOAD_FOLDER, 'local'),
            os.path.join(Config.UPLOAD_FOLDER, 'online')
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)

    @classmethod
    def init_app(cls, app):
        """初始化应用配置"""
        # 确保上传目录存在
        cls.init_upload_folder()

        # 配置日志
        import logging
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format=cls.LOG_FORMAT
        )