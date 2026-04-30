# 测试 http 模式
IMA_MCP_MODE=http ima-mcp
```

## 版本历史

- **1.0.1**：上传到 PyPI
  - 修复历史提交者信息，统一使用 Du Hanjun
  - 更新项目文档和注释
  - 优化 MCP 客户端配置说明
  - 添加 stdio 和 http 两种模式的完整配置示例

- **1.0.0**：初始版本
  - 支持知识库管理
  - 支持笔记管理
  - 支持文件上传
  - 支持批量操作
  - 集成缓存机制
  - 支持 stdio 和 http 两种接入方式
  - 本地部署默认使用 stdio 模式
  - Docker 部署默认使用 http 模式
  - 新增 HTTP API 文档和健康检查端点
