#!/usr/bin/env python3
"""
使用 MCP 服务查询知识库列表
"""

from ima_mcp.knowledge_base import KnowledgeBase

def list_knowledge_bases():
    """查询并显示知识库列表"""
    print("查询知识库列表...")
    print("=" * 60)
    
    try:
        # 初始化知识库模块
        kb = KnowledgeBase()
        
        # 查询知识库列表
        knowledge_bases = kb.list_knowledge_bases(limit=20)
        
        if knowledge_bases:
            print(f"找到 {len(knowledge_bases)} 个知识库：")
            print("-" * 60)
            
            for i, kb_info in enumerate(knowledge_bases, 1):
                name = kb_info.get('kb_name', '未知名称')
                kb_id = kb_info.get('id', '未知ID')
                base_type = kb_info.get('base_type', '未知类型')
                
                print(f"{i}. {name}")
                print(f"   ID: {kb_id}")
                print(f"   类型: {base_type}")
                print("-" * 60)
        else:
            print("没有找到知识库")
            
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    list_knowledge_bases()
