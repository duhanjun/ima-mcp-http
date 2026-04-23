#!/usr/bin/env python3
"""
IMA MCP 服务的标准 stdio 入口点
支持通过标准输入输出进行交互
"""

import sys
import json
from ima_mcp.client import IMAClient
from ima_mcp.knowledge_base import KnowledgeBase
from ima_mcp.notes import Notes

def process_request(request):
    """处理请求并返回响应"""
    try:
        # 解析请求
        data = json.loads(request)
        tool_name = data.get('toolcall', {}).get('name')
        params = data.get('toolcall', {}).get('params', {})
        
        # 初始化服务
        client = IMAClient()
        kb = KnowledgeBase()
        notes = Notes()
        
        # 处理不同的工具调用
        if tool_name == 'check_credentials':
            result = client.check_credentials()
        elif tool_name == 'list_knowledge_bases':
            limit = params.get('limit', 10)
            result = kb.list_knowledge_bases(limit=limit)
        elif tool_name == 'get_knowledge_base':
            knowledge_base_id = params.get('knowledge_base_id')
            result = kb.get_knowledge_base(knowledge_base_id)
        elif tool_name == 'search_knowledge':
            knowledge_base_id = params.get('knowledge_base_id')
            query = params.get('query')
            result = kb.search_knowledge(knowledge_base_id, query)
        elif tool_name == 'import_urls':
            knowledge_base_id = params.get('knowledge_base_id')
            urls = params.get('urls', [])
            result = kb.import_urls(knowledge_base_id, urls)
        elif tool_name == 'upload_file':
            knowledge_base_id = params.get('knowledge_base_id')
            file_path = params.get('file_path')
            result = kb.upload_file(knowledge_base_id, file_path)
        elif tool_name == 'batch_import_urls':
            knowledge_base_id = params.get('knowledge_base_id')
            urls = params.get('urls', [])
            result = kb.batch_import_urls(knowledge_base_id, urls)
        elif tool_name == 'batch_upload_files':
            knowledge_base_id = params.get('knowledge_base_id')
            file_paths = params.get('file_paths', [])
            result = kb.batch_upload_files(knowledge_base_id, file_paths)
        elif tool_name == 'batch_search_knowledge':
            knowledge_base_id = params.get('knowledge_base_id')
            queries = params.get('queries', [])
            result = kb.batch_search_knowledge(knowledge_base_id, queries)
        elif tool_name == 'search_notes':
            query = params.get('query')
            result = notes.search_notes(query)
        elif tool_name == 'create_note':
            title = params.get('title')
            content = params.get('content')
            result = notes.create_note(title, content)
        elif tool_name == 'append_note':
            note_id = params.get('note_id')
            content = params.get('content')
            result = notes.append_note(note_id, content)
        elif tool_name == 'get_note':
            note_id = params.get('note_id')
            result = notes.get_note(note_id)
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        # 构造响应
        response = {
            "toolcall_result": {
                "name": tool_name,
                "result": result
            }
        }
        
        return json.dumps(response, ensure_ascii=False, indent=2)
        
    except Exception as e:
        # 构造错误响应
        error_response = {
            "toolcall_result": {
                "name": tool_name,
                "error": str(e)
            }
        }
        return json.dumps(error_response, ensure_ascii=False, indent=2)

def main():
    """主函数"""
    # 从标准输入读取请求
    if not sys.stdin.isatty():
        # 非交互模式，从标准输入读取
        request = sys.stdin.read().strip()
        if request:
            response = process_request(request)
            print(response)
    else:
        # 交互模式，显示帮助信息
        print("IMA MCP 服务 - 标准 stdio 接口")
        print("=" * 60)
        print("使用方式:")
        print("1. 非交互模式: echo '{\"toolcall\": {\"name\": \"check_credentials\", \"params\": {}}}' | python main.py")
        print("2. 交互模式: 直接运行 python main.py (显示此帮助)")
        print("\n支持的工具:")
        print("- check_credentials: 检查凭证有效性")
        print("- list_knowledge_bases: 获取知识库列表")
        print("- get_knowledge_base: 获取知识库详情")
        print("- search_knowledge: 搜索知识库内容")
        print("- import_urls: 添加网页到知识库")
        print("- upload_file: 上传文件到知识库")
        print("- batch_import_urls: 批量添加网页")
        print("- batch_upload_files: 批量上传文件")
        print("- batch_search_knowledge: 批量搜索知识库")
        print("- search_notes: 搜索笔记")
        print("- create_note: 创建笔记")
        print("- append_note: 追加内容到笔记")
        print("- get_note: 获取笔记内容")

if __name__ == "__main__":
    main()
