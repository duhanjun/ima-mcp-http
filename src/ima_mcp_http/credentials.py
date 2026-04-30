import os
import os.path

class Credentials:
    """IMA 凭证管理"""
    
    def __init__(self):
        self.client_id = None
        self.api_key = None
        self.load_credentials()
    
    def load_credentials(self):
        """加载凭证，优先级：环境变量 > 配置文件"""
        # 从环境变量加载
        self.client_id = os.environ.get("IMA_OPENAPI_CLIENTID")
        self.api_key = os.environ.get("IMA_OPENAPI_APIKEY")
        
        # 如果环境变量未设置，从配置文件加载
        if not self.client_id or not self.api_key:
            config_path = os.path.expanduser("~/.config/ima")
            client_id_file = os.path.join(config_path, "client_id")
            api_key_file = os.path.join(config_path, "api_key")
            
            if os.path.exists(client_id_file):
                try:
                    with open(client_id_file, "r", encoding="utf-8") as f:
                        self.client_id = f.read().strip()
                except Exception:
                    pass
            
            if os.path.exists(api_key_file):
                try:
                    with open(api_key_file, "r", encoding="utf-8") as f:
                        self.api_key = f.read().strip()
                except Exception:
                    pass
    
    def is_valid(self):
        """检查凭证是否有效"""
        return bool(self.client_id and self.api_key)
    
    def get_headers(self, skill_version="1.1.3"):
        """获取 API 请求头"""
        if not self.is_valid():
            raise ValueError("缺少 IMA 凭证，请配置 Client ID 和 API Key")
        
        return {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "ima-openapi-ctx": f"skill_version={skill_version}",
            "Content-Type": "application/json"
        }
