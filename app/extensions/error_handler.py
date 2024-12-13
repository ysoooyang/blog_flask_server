from flask import jsonify, current_app
from werkzeug.exceptions import HTTPException
from app.utils.response import ErrorCode


def init_error_handlers(app):
    """初始化错误处理器"""

    @app.errorhandler(Exception)
    def handle_exception(error):
        """处理所有异常"""
        # 首先处理 HTTP 异常
        if isinstance(error, HTTPException):
            response = {
                'code': error.code,
                'message': error.description
            }
            return jsonify(response), error.code

        # 处理自定义错误码
        if hasattr(error, 'code'):
            status_code = 500

            # 根据错误码设置 HTTP 状态码
            if error.code == ErrorCode.AUTH:  # 没有权限
                status_code = 403
            elif error.code == ErrorCode.AUTHTOKEN:  # token 过期
                status_code = 401

            response = {
                'code': error.code,
                'message': str(error)
            }

            # 记录错误日志
            current_app.logger.error(
                f"Error {error.code}: {str(error)}",
                exc_info=True
            )

            return jsonify(response), status_code

        # 处理未预期的异常
        current_app.logger.error(
            "Unhandled Exception",
            exc_info=True
        )

        response = {
            'code': ErrorCode.SYSTEM,
            'message': '服务器内部错误'
        }

        # 在开发环境下返回详细错误信息
        if app.debug:
            response['debug_message'] = str(error)
            response['traceback'] = error.__traceback__

        return jsonify(response), 500

    @app.errorhandler(404)
    def not_found_error(error):
        """处理 404 错误"""
        response = {
            'code': ErrorCode.NOTFOUND,
            'message': '请求的资源不存在'
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """处理 405 错误"""
        response = {
            'code': ErrorCode.METHODNOTALLOWED,
            'message': '不支持的请求方法'
        }
        return jsonify(response), 405

    @app.errorhandler(429)
    def ratelimit_error(error):
        """处理请求限制错误"""
        response = {
            'code': ErrorCode.RATELIMIT,
            'message': '请求过于频繁，请稍后再试'
        }
        return jsonify(response), 429