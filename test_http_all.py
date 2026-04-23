#!/usr/bin/env python3
"""
测试 HTTP 模式的所有功能
"""

import os
import sys
import json
import time
import subprocess
import requests

def start_http_server():
    """启动 HTTP 服务器"""
    env = os.environ.copy()
    env['IMA_OPENAPI_APIKEY'] = 'y0mhfh3Fo0INSlQBXrqwVl+JaPNgrT2sEIsADmPko03zYd7jVi6QrdlNpLvEkE9UnqQsFdXAfA=='
    env['IMA_OPENAPI_CLIENTID'] = '0ebb2a4263625e43b2b8231cd2ec0a03'
    env['IMA_MCP_MODE'] = 'http'
    env['IMA_MCP_HOST'] = '127.0.0.1'
    env['IMA_MCP_PORT'] = '8001'
    
    print("启动 HTTP 服务器...")
    process = subprocess.Popen(
        ['ima-mcp'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待服务器启动
    time.sleep(3)
    
    # 检查服务器是否启动
    try:
        response = requests.get('http://127.0.0.1:8001/health', timeout=5)
        if response.status_code == 200:
            print("✅ HTTP 服务器启动成功")
            return process
        else:
            print("❌ HTTP 服务器启动失败")
            process.terminate()
            return None
    except Exception as e:
        print(f"❌ HTTP 服务器启动失败: {e}")
        process.terminate()
        return None

def run_http_command(tool_name, params=None):
    """运行 HTTP 模式的命令"""
    if params is None:
        params = {}
    
    url = 'http://127.0.0.1:8001/toolcall'
    data = {
        "toolcall": {
            "name": tool_name,
            "params": params
        }
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': f'HTTP error: {response.status_code}', 'content': response.text}
    except Exception as e:
        return {'error': f'Request failed: {e}'}

def test_all_functions():
    """测试所有功能"""
    print("测试 HTTP 模式的所有功能...")
    print("=" * 60)
    
    # 启动 HTTP 服务器
    server_process = start_http_server()
    if not server_process:
        return False
    
    try:
        tests = [
            # 凭证管理
            ('check_credentials', {}, '检查凭证有效性'),
            
            # 知识库管理
            ('list_knowledge_bases', {'limit': 5}, '获取知识库列表'),
            
            # 笔记管理
            ('search_notes', {'query': '测试'}, '搜索笔记'),
            ('create_note', {'title': 'HTTP测试笔记', 'content': '这是HTTP测试笔记内容'}, '创建笔记'),
        ]
        
        results = []
        for tool_name, params, description in tests:
            print(f"\n测试: {description}")
            print(f"工具: {tool_name}")
            print(f"参数: {json.dumps(params, ensure_ascii=False)}")
            
            response = run_http_command(tool_name, params)
            
            print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            if 'error' in response:
                print(f"❌ 失败: {response['error']}")
                results.append((tool_name, False, response['error']))
            else:
                if 'toolcall_result' in response:
                    tool_result = response['toolcall_result']
                    if 'error' not in tool_result or tool_result['error'] is None:
                        print(f"✅ 成功")
                        if 'result' in tool_result:
                            result_data = tool_result['result']
                            if isinstance(result_data, list):
                                print(f"  结果数量: {len(result_data)}")
                            elif isinstance(result_data, dict):
                                if 'valid' in result_data:
                                    print(f"  凭证状态: {'有效' if result_data['valid'] else '无效'}")
                                elif 'note_id' in result_data:
                                    print(f"  笔记ID: {result_data['note_id']}")
                        results.append((tool_name, True, None))
                    else:
                        error_msg = tool_result.get('error', '未知错误')
                        print(f"❌ 失败: {error_msg}")
                        results.append((tool_name, False, error_msg))
                else:
                    print(f"❌ 失败: 响应格式错误")
                    results.append((tool_name, False, '响应格式错误'))
            
            print("-" * 40)
        
        # 统计结果
        print("\n测试结果汇总:")
        print("=" * 60)
        passed = sum(1 for _, success, _ in results if success)
        failed = len(results) - passed
        
        print(f"总测试数: {len(results)}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        
        if failed > 0:
            print("\n失败的测试:")
            for tool_name, _, error in results:
                if not _:
                    print(f"- {tool_name}: {error}")
        
        return passed == len(results)
        
    finally:
        # 停止服务器
        if server_process:
            server_process.terminate()
            print("\nHTTP 服务器已停止")

if __name__ == "__main__":
    success = test_all_functions()
    sys.exit(0 if success else 1)
