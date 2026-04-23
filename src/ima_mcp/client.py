import requests
from .credentials import Credentials

class IMAClient:
    """IMA API 客户端"""
    
    BASE_URL = "https://ima.qq.com"
    
    def __init__(self):
        self.credentials = Credentials()
        self.session = requests.Session()
    
    def _request(self, path, data=None):
        """发送 API 请求"""
        url = f"{self.BASE_URL}/{path}"
        headers = self.credentials.get_headers()
        
        try:
            response = self.session.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 请求失败: {str(e)}")
    
    def check_credentials(self):
        """检查凭证有效性"""
        if not self.credentials.is_valid():
            return {"valid": False, "message": "缺少 IMA 凭证"}
        
        try:
            # 发送一个轻量级请求来验证凭证
            response = self._request("openapi/wiki/v1/search_knowledge_base", {
                "query": "",
                "cursor": "",
                "limit": 1
            })
            return {"valid": True, "message": "凭证有效"}
        except Exception as e:
            return {"valid": False, "message": f"凭证无效: {str(e)}"}
