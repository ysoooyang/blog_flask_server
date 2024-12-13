from functools import wraps
from flask import request, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.utils.response import error_response, ErrorCode


class RateLimitConfig:
    """速率限制配置"""

    def __init__(self,
                 interval: int = 60,  # 默认1分钟
                 max_requests: int = 10,  # 默认最多10次请求
                 prefix_key: str = None,  # 端点前缀
                 message: str = "请求过于频繁，请稍后再试"):
        if not prefix_key:
            raise ValueError("TimesLimiterError, prefix_key is required")

        self.interval = interval
        self.max_requests = max_requests
        self.prefix_key = prefix_key
        self.message = message


def create_limiter(app):
    """创建限流器"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    return limiter


def rate_limit(config: RateLimitConfig = None):
    """创建速率限制装饰器"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not config:
                return f(*args, **kwargs)

            # 获取请求IP
            ip = request.headers.get('X-Real-IP') or \
                 request.headers.get('X-Forwarded-For') or \
                 request.remote_addr

            # 获取限流器
            limiter = current_app.extensions.get('limiter')
            if not limiter:
                current_app.logger.warning("Limiter not initialized")
                return f(*args, **kwargs)

            # 创建限流键
            key = f"{config.prefix_key}:{ip}"

            # 检查是否超过限制
            if not limiter.check():
                current_app.logger.warning(f"Rate limit exceeded for IP: {ip}")
                return error_response(
                    ErrorCode.TIPS,
                    config.message
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def create_times_limiter(
        prefix_key: str,
        interval: int = 60,
        max_requests: int = 10,
        message: str = "请求过于频繁，请稍后再试"
):
    """创建次数限制器

    Args:
        prefix_key: 端点前缀，用于区分不同的接口
        interval: 时间间隔（秒）
        max_requests: 最大请求次数
        message: 超出限制时的提示消息

    Returns:
        装饰器函数
    """
    config = RateLimitConfig(
        interval=interval,
        max_requests=max_requests,
        prefix_key=prefix_key,
        message=message
    )
    return rate_limit(config)