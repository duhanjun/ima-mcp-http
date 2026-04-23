#!/usr/bin/env python3
"""
IMA MCP 服务的 HTTP 服务器入口点
支持通过 HTTP API 进行交互
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from ima_mcp.client import IMAClient
from ima_mcp.knowledge_base import KnowledgeBase
from ima_mcp.notes import Notes

# 初始化 FastAPI 应用
app = FastAPI(title="IMA MCP HTTP Server", description="IMA OpenAPI MCP Service - HTTP Mode", version="1.0.0")

# 初始化服务
client = IMAClient()
kb = KnowledgeBase()
notes = Notes()

# 定义请求和响应模型
class ToolCallRequest(BaseModel):
    name: str = Field(..., description="工具名称")
    params: Dict[str, Any] = Field(default_factory=dict, description="工具参数")

class MCPRequest(BaseModel):
    toolcall: ToolCallRequest = Field(..., description="工具调用请求")

class ToolCallResult(BaseModel):
    name: str = Field(..., description="工具名称")
    result: Optional[Any] = Field(None, description="工具执行结果")
    error: Optional[str] = Field(None, description="错误信息")

class MCPResponse(BaseModel):
    toolcall_result: ToolCallResult = Field(..., description="工具调用结果")

def process_request(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """处理工具调用请求并返回结果"""
    try:
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
            return {"name": tool_name, "error": f"Unknown tool: {tool_name}"}
        
        return {"name": tool_name, "result": result}
        
    except Exception as e:
        return {"name": tool_name, "error": str(e)}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "ima-mcp-http-server"}

@app.get("/")
async def root():
    """根端点，显示服务信息"""
    return {
        "service": "IMA MCP HTTP Server",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "toolcall": "/toolcall",
            "docs": "/docs"
        }
    }

@app.post("/toolcall", response_model=MCPResponse)
async def toolcall(request: MCPRequest):
    """工具调用端点"""
    result = process_request(request.toolcall.name, request.toolcall.params)
    return {"toolcall_result": result}

def start_http_server(host: str = "0.0.0.0", port: int = 8000):
    """启动 HTTP 服务器"""
    import uvicorn
    print(f"Starting IMA MCP HTTP Server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    host = os.getenv("IMA_MCP_HOST", "0.0.0.0")
    port = int(os.getenv("IMA_MCP_PORT", "8000"))
    start_http_server(host, port)
