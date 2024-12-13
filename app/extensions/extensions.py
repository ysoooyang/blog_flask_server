# app/extensions/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 数据库
db = SQLAlchemy()

# 数据库迁移
migrate = Migrate()

# JWT
jwt = JWTManager()

# 跨域
cors = CORS()

# 限流器
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)