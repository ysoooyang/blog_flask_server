from flask import Flask
from .error_handler import init_error_handlers

def init_extensions(app: Flask):
    """初始化所有扩展"""
    # 初始化错误处理
    init_error_handlers(app)