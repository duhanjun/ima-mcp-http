from .client import IMAClient
from .cache import cache

class KnowledgeBase:
    """知识库模块"""
    
    def __init__(self):
        self.client = IMAClient()
    
    def list_knowledge_bases(self, limit=20):
        """获取知识库列表"""
        # 生成缓存键
        cache_key = f"knowledge_bases_{limit}"
        
        # 尝试从缓存获取
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 缓存未命中，调用 API
        response = self.client._request("openapi/wiki/v1/search_knowledge_base", {
            "query": "",
            "cursor": "",
            "limit": min(limit, 20)  # 限制最多20个
        })
        
        if response.get("code") == 0:
            result = response.get("data", {}).get("info_list", [])
            # 缓存结果
            cache.set(cache_key, result)
            return result
        else:
            raise Exception(f"获取知识库列表失败: {response.get('msg', '未知错误')}")
    
    def get_knowledge_base(self, knowledge_base_id):
        """获取知识库详情"""
        # 生成缓存键
        cache_key = f"knowledge_base_{knowledge_base_id}"
        
        # 尝试从缓存获取
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 缓存未命中，调用 API
        response = self.client._request("openapi/wiki/v1/get_knowledge_base", {
            "ids": [knowledge_base_id]
        })
        
        if response.get("code") == 0:
            infos = response.get("data", {}).get("infos", {})
            result = infos.get(knowledge_base_id)
            # 缓存结果
            cache.set(cache_key, result)
            return result
        else:
            raise Exception(f"获取知识库详情失败: {response.get('msg', '未知错误')}")
    
    def search_knowledge(self, knowledge_base_id, query, limit=20):
        """在知识库中搜索内容"""
        response = self.client._request("openapi/wiki/v1/search_knowledge", {
            "knowledge_base_id": knowledge_base_id,
            "query": query,
            "cursor": "",
            "limit": min(limit, 20)
        })
        
        if response.get("code") == 0:
            return response.get("data", {}).get("info_list", [])
        else:
            raise Exception(f"搜索知识库失败: {response.get('msg', '未知错误')}")
    
    def import_urls(self, knowledge_base_id, urls, folder_id=None):
        """添加网页到知识库"""
        data = {
            "knowledge_base_id": knowledge_base_id,
            "urls": urls
        }
        if folder_id:
            data["folder_id"] = folder_id
        
        response = self.client._request("openapi/wiki/v1/import_urls", data)
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"添加网页失败: {response.get('msg', '未知错误')}")
    
    def check_repeated_names(self, knowledge_base_id, file_names, media_types, folder_id=None):
        """检查文件名是否重复"""
        params = []
        for name, media_type in zip(file_names, media_types):
            params.append({"name": name, "media_type": media_type})
        
        data = {
            "params": params,
            "knowledge_base_id": knowledge_base_id
        }
        if folder_id:
            data["folder_id"] = folder_id
        
        response = self.client._request("openapi/wiki/v1/check_repeated_names", data)
        
        if response.get("code") == 0:
            return response.get("data", {}).get("results", [])
        else:
            raise Exception(f"检查文件名重复失败: {response.get('msg', '未知错误')}")
    
    def create_media(self, knowledge_base_id, file_name, file_size, content_type, file_ext):
        """创建媒体"""
        data = {
            "file_name": file_name,
            "file_size": file_size,
            "content_type": content_type,
            "knowledge_base_id": knowledge_base_id,
            "file_ext": file_ext
        }
        
        response = self.client._request("openapi/wiki/v1/create_media", data)
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"创建媒体失败: {response.get('msg', '未知错误')}")
    
    def add_knowledge(self, knowledge_base_id, media_type, media_id, title, file_info, folder_id=None):
        """添加知识到知识库"""
        data = {
            "media_type": media_type,
            "media_id": media_id,
            "title": title,
            "knowledge_base_id": knowledge_base_id,
            "file_info": file_info
        }
        if folder_id:
            data["folder_id"] = folder_id
        
        response = self.client._request("openapi/wiki/v1/add_knowledge", data)
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"添加知识失败: {response.get('msg', '未知错误')}")
    
    def upload_file(self, knowledge_base_id, file_path, folder_id=None):
        """上传文件到知识库"""
        import os
        import mimetypes
        
        # 获取文件信息
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_ext = os.path.splitext(file_name)[1][1:] if os.path.splitext(file_name)[1] else ""
        
        # 自动检测 MIME 类型
        content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        
        # 映射媒体类型
        media_type_map = {
            "pdf": 1,
            "doc": 3, "docx": 3,
            "ppt": 4, "pptx": 4,
            "xls": 5, "xlsx": 5, "csv": 5,
            "md": 7, "markdown": 7,
            "png": 9, "jpg": 9, "jpeg": 9, "webp": 9,
            "txt": 13,
            "xmind": 14,
            "mp3": 15, "m4a": 15, "wav": 15, "aac": 15
        }
        media_type = media_type_map.get(file_ext.lower(), 13)  # 默认文本类型
        
        # 检查文件名是否重复
        repeated = self.check_repeated_names(knowledge_base_id, [file_name], [media_type], folder_id)
        if repeated and repeated[0].get("is_repeated"):
            # 如果文件名重复，添加时间戳
            import time
            timestamp = time.strftime("%Y%m%d%H%M%S")
            name_part, ext_part = os.path.splitext(file_name)
            file_name = f"{name_part}_{timestamp}{ext_part}"
        
        # 创建媒体
        media_result = self.create_media(knowledge_base_id, file_name, file_size, content_type, file_ext)
        media_id = media_result.get("media_id")
        cos_credential = media_result.get("cos_credential")
        
        if not media_id or not cos_credential:
            raise Exception("创建媒体失败，缺少必要参数")
        
        # 上传到 COS
        try:
            print(f"正在上传文件 {file_name} 到 COS...")
            
            # 提取 COS 凭证
            secret_id = cos_credential.get("secret_id")
            secret_key = cos_credential.get("secret_key")
            token = cos_credential.get("token")
            bucket = cos_credential.get("bucket_name")
            region = cos_credential.get("region")
            cos_key = cos_credential.get("cos_key")
            start_time = cos_credential.get("start_time")
            expired_time = cos_credential.get("expired_time")
            
            # 构建 COS 上传 URL
            hostname = f"{bucket}.cos.{region}.myqcloud.com"
            pathname = f"/{cos_key}"
            cos_url = f"https://{hostname}{pathname}"
            
            # 读取文件内容
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # 构建签名
            import hmac
            import hashlib
            import urllib.parse
            
            # 1. 计算 KeyTime
            key_time = f"{start_time};{expired_time}"
            
            # 2. 计算 SignKey
            sign_key = hmac.new(secret_key.encode('utf-8'), key_time.encode('utf-8'), hashlib.sha1).hexdigest()
            
            # 3. 构建 HttpString
            method = "PUT"
            headers = {
                "content-length": str(len(file_content)),
                "host": hostname
            }
            header_keys = sorted(headers.keys())
            http_headers = '&'.join([f"{k.lower()}={urllib.parse.quote(headers[k])}" for k in header_keys])
            http_string = f"{method.lower()}\n{pathname}\n\n{http_headers}\n"
            
            # 4. 计算 StringToSign
            string_to_sign = f"sha1\n{key_time}\n{hashlib.sha1(http_string.encode('utf-8')).hexdigest()}\n"
            
            # 5. 计算 Signature
            signature = hmac.new(sign_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()
            
            # 6. 构建 Authorization 头
            header_list = ';'.join([k.lower() for k in header_keys])
            authorization = (
                f"q-sign-algorithm=sha1&"
                f"q-ak={secret_id}&"
                f"q-sign-time={key_time}&"
                f"q-key-time={key_time}&"
                f"q-header-list={header_list}&"
                f"q-url-param-list=&"
                f"q-signature={signature}"
            )
            
            # 发送 PUT 请求
            import requests
            headers = {
                "Content-Type": content_type,
                "Content-Length": str(len(file_content)),
                "Authorization": authorization,
                "x-cos-security-token": token
            }
            
            response = requests.put(cos_url, data=file_content, headers=headers, timeout=30)
            response.raise_for_status()
            
            print(f"文件 {file_name} 上传到 COS 成功")
            
            # 添加到知识库
            file_info = {
                "cos_key": cos_key,
                "file_size": file_size,
                "file_name": file_name
            }
            
            return self.add_knowledge(knowledge_base_id, media_type, media_id, file_name, file_info, folder_id)
        except Exception as e:
            # 如果 COS 上传失败，提供详细的错误信息
            raise Exception(f"COS 上传失败: {str(e)}")
    
    def batch_import_urls(self, knowledge_base_id, urls_list, folder_id=None):
        """批量添加网页到知识库"""
        # 每次最多添加 10 个 URL
        batch_size = 10
        results = []
        
        for i in range(0, len(urls_list), batch_size):
            batch_urls = urls_list[i:i+batch_size]
            try:
                result = self.import_urls(knowledge_base_id, batch_urls, folder_id)
                results.append({
                    "urls": batch_urls,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "urls": batch_urls,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def batch_upload_files(self, knowledge_base_id, file_paths, folder_id=None):
        """批量上传文件到知识库"""
        results = []
        
        for file_path in file_paths:
            try:
                result = self.upload_file(knowledge_base_id, file_path, folder_id)
                results.append({
                    "file_path": file_path,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "file_path": file_path,
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def batch_search_knowledge(self, knowledge_base_id, queries):
        """批量搜索知识库"""
        results = []
        
        for query in queries:
            try:
                result = self.search_knowledge(knowledge_base_id, query, limit=10)
                results.append({
                    "query": query,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
        
        return results
