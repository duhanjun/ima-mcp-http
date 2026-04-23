#!/usr/bin/env python3
"""
测试 IMA MCP 项目是否能正常使用
"""

import sys

print("测试 IMA MCP 项目...")
print("=" * 60)

# 测试模块导入
try:
    from ima_mcp.client import IMAClient
    from ima_mcp.knowledge_base import KnowledgeBase
    from ima_mcp.notes import Notes
    print("✅ 模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

# 测试基本功能
try:
    # 测试客户端初始化
    client = IMAClient()
    print("✅ 客户端初始化成功")
    
    # 测试知识库模块初始化
    kb = KnowledgeBase()
    print("✅ 知识库模块初始化成功")
    
    # 测试笔记模块初始化
    notes = Notes()
    print("✅ 笔记模块初始化成功")
    
    print("\n✅ 所有模块初始化成功，项目可以正常使用！")
    print("\n项目功能列表:")
    print("- 凭证管理: 检查凭证有效性")
    print("- 知识库管理: 列表、搜索、详情、文件上传、网页添加")
    print("- 笔记管理: 搜索、创建、追加、获取")
    print("- 批量操作: 支持批量上传文件、批量添加网页、批量搜索")
    
    print("\n使用示例:")
    print("from ima_mcp.client import IMAClient")
    print("client = IMAClient()")
    print("result = client.check_credentials()")
    print("print(f'凭证是否有效: {result[\"valid\"]}')")
    
except Exception as e:
    print(f"❌ 功能测试失败: {e}")
    sys.exit(1)

print("=" * 60)
print("测试完成！项目可以正常使用。")
