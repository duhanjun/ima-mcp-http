from .client import IMAClient

class Notes:
    """笔记模块"""
    
    def __init__(self):
        self.client = IMAClient()
    
    def search_notes(self, query, limit=20):
        """搜索笔记"""
        response = self.client._request("openapi/note/v1/search_note_book", {
            "search_type": 0,  # 0=标题检索
            "query_info": {"title": query},
            "start": 0,
            "end": min(limit, 20)
        })
        
        if response.get("code") == 0:
            return response.get("data", {}).get("docs", [])
        else:
            raise Exception(f"搜索笔记失败: {response.get('msg', '未知错误')}")
    
    def create_note(self, title, content):
        """创建新笔记"""
        # 确保内容是 UTF-8 编码
        if isinstance(content, str):
            content = content.encode('utf-8', 'ignore').decode('utf-8')
        if isinstance(title, str):
            title = title.encode('utf-8', 'ignore').decode('utf-8')
        
        # 构造 Markdown 内容
        markdown_content = f"# {title}\n\n{content}"
        
        response = self.client._request("openapi/note/v1/import_doc", {
            "content_format": 1,  # 1 表示 Markdown
            "content": markdown_content
        })
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"创建笔记失败: {response.get('msg', '未知错误')}")
    
    def append_note(self, note_id, content):
        """追加内容到笔记"""
        # 确保内容是 UTF-8 编码
        if isinstance(content, str):
            content = content.encode('utf-8', 'ignore').decode('utf-8')
        
        response = self.client._request("openapi/note/v1/append_doc", {
            "doc_id": note_id,
            "content_format": 1,  # 1 表示 Markdown
            "content": f"\n{content}"
        })
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"追加笔记失败: {response.get('msg', '未知错误')}")
    
    def get_note(self, note_id):
        """获取笔记内容"""
        response = self.client._request("openapi/note/v1/get_doc_content", {
            "doc_id": note_id,
            "target_content_format": 0  # 0 表示纯文本
        })
        
        if response.get("code") == 0:
            return response.get("data", {})
        else:
            raise Exception(f"获取笔记失败: {response.get('msg', '未知错误')}")
