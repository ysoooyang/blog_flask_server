import random
import requests
from typing import Optional
from flask import current_app


def get_ip_address(ip: str) -> str:
    """
    使用 IP.SB API 查询 IP 地址信息
    """
    if not ip:
        return "本地地址"

    # 判断是否为内网IP
    if ip.startswith(('10.', '172.', '192.168.')):
        return "内网地址"

    try:
        # 使用 ip.sb 的 API（无需注册，免费使用）
        response = requests.get(f'https://api.ip.sb/geoip/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            country = data.get('country', '')
            city = data.get('city', '')
            if country and city:
                return f"{country}-{city}"
            elif country:
                return country

    except Exception as e:
        current_app.logger.error(f"IP地址查询失败: {str(e)}")

    return "未知地址"


def random_nickname(prefix: str = "", random_length: int = 8) -> str:
    """生成随机昵称"""
    name_arr = [
        list("1234567890"),
        list("abcdefghijklmnopqrstuvwxyz")
    ]

    name = prefix
    for _ in range(random_length):
        index = random.randint(0, 1)
        name += random.choice(name_arr[index])

    return name


def get_current_type_name(type_: str) -> str:
    """获取当前类型名称"""
    type_map = {
        "1": "文章",
        "2": "说说",
        "3": "留言"
    }
    return type_map.get(str(type_), "0")


def is_valid_url(url: str) -> bool:
    """判断URL是否包含http/https"""
    return 'http' in url or 'https' in url