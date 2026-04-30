import json
import os

class JSONEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，处理特殊类型"""
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', 'ignore')
        return super().default(obj)

def format_response(data, success=True, message=""):
    """格式化响应"""
    return {
        "success": success,
        "message": message,
        "data": data
    }

def ensure_utf8(string):
    """确保字符串是 UTF-8 编码"""
    if isinstance(string, str):
        return string.encode('utf-8', 'ignore').decode('utf-8')
    return string
