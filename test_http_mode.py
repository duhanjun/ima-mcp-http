#!/usr/bin/env python3
"""
测试 HTTP 模式的基本功能
"""
import os
import sys
import time
import subprocess
import requests
import json

def test_http_server():
    """测试HTTP服务器"""
    print("测试 HTTP 模式基本功能...")
    
    # 测试环境变量配置
    print("\n1. 测试环境变量配置...")
    os.environ['IMA_OPENAPI_APIKEY'] = 'y0mhfh3Fo0INSlQBXrqwVl+JaPNgrT2sEIsADmPko03zYd7jVi6QrdlNpLvEkE9UnqQsFdXAfA=='
    os.environ['IMA_OPENAPI_CLIENTID'] = '0ebb2a4263625e43b2b8231cd2ec0a03'
    os.environ['IMA_MCP_MODE'] = 'http'
    os.environ['IMA_MCP_HOST'] = '127.0.0.1'
    os.environ['IMA_MCP_PORT'] = '8001'
    
    print(f"IMA_MCP_MODE: {os.getenv('IMA_MCP_MODE')}")
    print(f"IMA_MCP_HOST: {os.getenv('IMA_MCP_HOST')}")
    print(f"IMA_MCP_PORT: {os.getenv('IMA_MCP_PORT')}")
    
    # 测试HTTP服务器模块导入
    print("\n2. 测试HTTP服务器模块导入...")
    try:
        from ima_mcp import http_server
        print("✓ HTTP服务器模块导入成功")
    except Exception as e:
        print(f"✗ HTTP服务器模块导入失败: {e}")
        return False
    
    # 测试process_request函数
    print("\n3. 测试工具调用函数...")
    try:
        from ima_mcp.main import process_request
        result = process_request("check_credentials", {})
        print(f"✓ 工具调用成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"✗ 工具调用失败: {e}")
        return False
    
    print("\n✓ HTTP模式基本功能测试通过！")
    print("\nHTTP服务器启动命令：")
    print("IMA_MCP_MODE=http IMA_MCP_PORT=8000 ima-mcp")
    print("\n或者使用uvx：")
    print("IMA_MCP_MODE=http IMA_MCP_PORT=8000 uvx --with-editable . ima-mcp")
    print("\nHTTP API使用示例：")
    print("curl -X POST http://localhost:8000/toolcall -H 'Content-Type: application/json' -d '{\"toolcall\": {\"name\": \"check_credentials\", \"params\": {}}}'")
    
    return True

if __name__ == "__main__":
    success = test_http_server()
    sys.exit(0 if success else 1)
