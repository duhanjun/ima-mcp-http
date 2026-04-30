#!/usr/bin/env python3
"""
IMA MCP 服务的主入口点
支持 stdio 和 http 两种接入方式
默认使用 stdio 模式
"""

import os
import sys
import json

from ima_mcp_http.client import IMAClient
from ima_mcp_http.knowledge_base import KnowledgeBase
from ima_mcp_http.notes import Notes

def process_request(tool_name: str, params: dict) -> dict:
    """处理请求并返回响应"""
    try:
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
        
        return response
        
    except Exception as e:
        # 构造错误响应
        error_response = {
            "toolcall_result": {
                "name": tool_name,
                "error": str(e)
            }
        }
        return error_response

def run_stdio_mode():
    """运行 stdio 模式"""
    print("IMA MCP 服务 - stdio 模式")
    print("=" * 60)
    
    # 从标准输入读取请求
    if not sys.stdin.isatty():
        # 非交互模式，从标准输入读取
        request = sys.stdin.read().strip()
        if request:
            data = json.loads(request)
            tool_name = data.get('toolcall', {}).get('name')
            params = data.get('toolcall', {}).get('params', {})
            response = process_request(tool_name, params)
            print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        # 交互模式，显示帮助信息
        print("使用方式:")
        print("1. 非交互模式: echo '{\"toolcall\": {\"name\": \"check_credentials\", \"params\": {}}}' | ima-mcp")
        print("2. 交互模式: 直接运行 ima-mcp (显示此帮助)")
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

def run_http_mode():
    """运行 http 模式"""
    from ima_mcp_http.http_server import start_http_server
    host = os.getenv("IMA_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("IMA_MCP_PORT", "8000"))
    start_http_server(host, port)

def main():
    """主函数"""
    # 获取运行模式，默认使用 stdio
    mode = os.getenv("IMA_MCP_MODE", "stdio").lower()
    
    if mode == "http":
        run_http_mode()
    else:
        # 默认使用 stdio 模式
        run_stdio_mode()

if __name__ == "__main__":
    main()
