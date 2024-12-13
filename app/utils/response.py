from typing import Any, Dict, Optional, Union
from flask import jsonify


class ErrorCode:
    USER = "100001"
    AUTH = "100002"
    TAG = "100003"
    CATEGORY = "100004"
    ARTICLE = "100005"
    UPLOAD = "100006"
    CONFIG = "100007"
    STATISTIC = "100008"
    PHOTOALBUM = "100009"
    PHOTO = "100010"
    TALK = "100011"
    MESSAGE = "100012"
    RECOMMEND = "100012"
    HEADER = "100013"
    LINKS = "100014"
    COMMENT = "100015"
    AUTHTOKEN = "100016"
    NOTIFY = "100017"
    LIKE = "100018"
    CHAT = "100019"
    TIPS = "111111"
    NOTFOUND = "200001"
    SYSTEM = "200002"


def success_response(message: str = "Success", data: Any = None) -> Dict:
    """成功响应

    Args:
        message: 成功消息
        data: 响应数据

    Returns:
        Dict: 响应字典
    """
    return jsonify({
        "code": 0,
        "message": message,
        "result": data
    })


def tips_response(message: str) -> Dict:
    """提示响应

    Args:
        message: 提示消息

    Returns:
        Dict: 响应字典
    """
    return jsonify({
        "code": ErrorCode.TIPS,
        "message": message
    })


def error_response(
        message: str,
        code: Union[str, ErrorCode],
        status_code: int = 400
) -> tuple[Dict, int]:
    """错误响应

    Args:
        message: 错误消息
        code: 错误代码
        status_code: HTTP状态码

    Returns:
        tuple: (响应字典, HTTP状态码)
    """
    return jsonify({
        "code": code,
        "message": message,
        "success": False
    }), status_code


def throw_error(code: Union[str, ErrorCode], message: str) -> tuple[Dict, int]:
    """抛出错误（用于中间件）

    Args:
        code: 错误代码
        message: 错误消息

    Returns:
        tuple: (响应字典, HTTP状态码)
    """
    return error_response(message, code)