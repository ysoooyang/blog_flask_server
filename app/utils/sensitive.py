import re
import requests
from typing import Optional


class SimpleFilter:
    def __init__(self, words):
        self.words = set(words)

    def filter(self, text: str) -> str:
        """过滤敏感词"""
        if not text:
            return text

        result = text
        for word in self.words:
            if word in result:
                result = result.replace(word, '*' * len(word))
        return result


# 敏感词列表
SENSITIVE_WORDS = [
    "我是你爸爸", "我是你爸", "我是你爹", "爸爸",
    "我是你爷爷", "操你奶奶", "我是你妈", "我日你爸",
    "草泥马", "草你妈", "操你妈", "傻逼"
]

# XSS防护
BAD_JS_PATTERN = re.compile(
    r'script|alert|window|prompt|location|href|iframe|onload|onerror',
    re.IGNORECASE
)


def get_saying() -> str:
    """获取每日一句"""
    try:
        response = requests.get("https://open.iciba.com/dsapi/", timeout=5)
        if response.status_code == 200:
            return response.json()['note']
    except Exception as e:
        print(f"Error fetching saying: {e}")
    return "今天天气真好"


def filter_sensitive(text: str) -> str:
    """过滤敏感词"""
    if not text:
        return text

    # 创建过滤器实例
    word_filter = SimpleFilter(SENSITIVE_WORDS)
    filtered_text = word_filter.filter(text)

    # 如果包含敏感词或JS代码，返回每日一句
    if '*' in filtered_text or BAD_JS_PATTERN.search(text):
        return get_saying()

    return filtered_text