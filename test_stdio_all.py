#!/usr/bin/env python3
"""
测试 stdio 模式的所有功能
"""

import os
import sys
import json
import subprocess

def run_stdio_command(tool_name, params=None):
    """运行 stdio 模式的命令"""
    if params is None:
        params = {}
    
    request = {
        "toolcall": {
            "name": tool_name,
            "params": params
        }
    }
    
    # 构造命令
    env = os.environ.copy()
    env['IMA_OPENAPI_APIKEY'] = 'y0mhfh3Fo0INSlQBXrqwVl+JaPNgrT2sEIsADmPko03zYd7jVi6QrdlNpLvEkE9UnqQsFdXAfA=='
    env['IMA_OPENAPI_CLIENTID'] = '0ebb2a4263625e43b2b8231cd2ec0a03'
    env['IMA_MCP_MODE'] = 'stdio'
    
    # 运行命令
    cmd = ['ima-mcp']
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    # 发送请求
    stdout, stderr = process.communicate(json.dumps(request))
    
    if process.returncode != 0:
        return {'error': f'Command failed with return code {process.returncode}', 'stderr': stderr}
    
    # 解析响应
    try:
        # 提取 JSON 部分
        json_start = stdout.find('{')
        if json_start != -1:
            response_str = stdout[json_start:]
            response = json.loads(response_str)
            return response
        else:
            return {'error': 'No JSON response found', 'stdout': stdout}
    except json.JSONDecodeError as e:
        return {'error': f'Failed to parse JSON: {e}', 'stdout': stdout}

def test_all_functions():
    """测试所有功能"""
    print("测试 stdio 模式的所有功能...")
    print("=" * 60)
    
    tests = [
        # 凭证管理
        ('check_credentials', {}, '检查凭证有效性'),
        
        # 知识库管理
        ('list_knowledge_bases', {'limit': 5}, '获取知识库列表'),
        
        # 笔记管理
        ('search_notes', {'query': '测试'}, '搜索笔记'),
        ('create_note', {'title': '测试笔记', 'content': '这是测试笔记内容'}, '创建笔记'),
    ]
    
    results = []
    for tool_name, params, description in tests:
        print(f"\n测试: {description}")
        print(f"工具: {tool_name}")
        print(f"参数: {json.dumps(params, ensure_ascii=False)}")
        
        response = run_stdio_command(tool_name, params)
        
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

if __name__ == "__main__":
    success = test_all_functions()
    sys.exit(0 if success else 1)
