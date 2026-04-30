# IMA MCP Service

统一的 IMA OpenAPI MCP 服务，支持笔记管理和知识库操作，提供 stdio 和 http 两种接入方式。

## 项目结构

```
ima-mcp/
├── README.md              # 项目说明
├── requirements.txt       # 依赖管理
├── Dockerfile             # Docker 配置
├── docker-compose.yml     # Docker Compose 配置
└── src/                   # 源代码目录
    └── ima_mcp/           # 主包
        ├── __init__.py    # 包初始化
        ├── main.py        # 主入口点（支持 stdio 和 http）
        ├── http_server.py # HTTP 服务器
        ├── client.py      # IMA API 客户端
        ├── credentials.py # 凭证管理
        ├── knowledge_base.py  # 知识库模块
        ├── notes.py       # 笔记模块
        ├── utils.py       # 工具函数
        └── mcp/           # MCP 服务配置
            ├── SERVER_METADATA.json  # 服务配置
            └── tools/     # 工具定义
```

## 功能特性

- **知识库管理**：列表、搜索、详情、文件上传、网页添加
- **笔记管理**：搜索、创建、追加、获取
- **凭证管理**：支持环境变量和配置文件
- **编码处理**：自动 UTF-8 编码校验
- **跨平台兼容**：支持 Windows、macOS、Linux
- **批量操作**：支持批量上传文件、批量添加网页、批量搜索
- **缓存机制**：内置内存缓存和文件缓存，提高响应速度
- **多种接入方式**：支持 stdio 和 http 两种接入方式

## 环境要求

- Python 3.7+
- requests 库
- urllib3 库
- fastapi 库（HTTP模式）
- uvicorn 库（HTTP模式）
- pydantic 库（HTTP模式）

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 配置凭证
# 方式 1: 环境变量
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"

# 方式 2: 配置文件
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key
```

## 接入方式

项目支持两种接入方式：stdio 模式（本地部署默认）和 http 模式（Docker部署默认）。

### 1. stdio 模式（默认）

适合本地开发和直接集成到 MCP 客户端。

#### MCP 客户端配置

在您的 MCP 客户端配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "ima-mcp": {
      "command": "uvx",
      "args": [
        "ima-mcp"
      ],
      "env": {
        "IMA_OPENAPI_CLIENTID": "your_client_id",
        "IMA_OPENAPI_APIKEY": "your_api_key"
      }
    }
  }
}
```

#### 直接运行方式

```bash
# 配置环境变量
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"

# 直接运行（默认使用 stdio 模式）
ima-mcp

# 或者显式指定
IMA_MCP_MODE=stdio ima-mcp

# 使用 uvx 运行
uvx --with-editable . ima-mcp
```

### 2. http 模式

适合作为独立服务部署，提供 HTTP API。

```bash
# 配置环境变量
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"
export IMA_MCP_MODE=http
export IMA_MCP_HOST=0.0.0.0
export IMA_MCP_PORT=8000

# 运行 HTTP 服务器
ima-mcp
```

#### HTTP API 使用示例

```bash
# 健康检查
curl http://localhost:8000/health

# 查看服务信息
curl http://localhost:8000/

# 检查凭证
curl -X POST http://localhost:8000/toolcall \
  -H "Content-Type: application/json" \
  -d '{
    "toolcall": {
      "name": "check_credentials",
      "params": {}
    }
  }'

# 获取知识库列表
curl -X POST http://localhost:8000/toolcall \
  -H "Content-Type: application/json" \
  -d '{
    "toolcall": {
      "name": "list_knowledge_bases",
      "params": {
        "limit": 10
      }
    }
  }'
```

### 3. Docker 部署（默认使用 http 模式）

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写您的 IMA OpenAPI 凭证

# 2. 构建并启动容器
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止容器
docker-compose down
```

或者使用 Docker 命令：

```bash
# 构建镜像
docker build -t ima-mcp .

# 运行容器
docker run -d \
  --name ima-mcp \
  -p 8000:8000 \
  -e IMA_OPENAPI_CLIENTID="your_client_id" \
  -e IMA_OPENAPI_APIKEY="your_api_key" \
  -e IMA_MCP_MODE=http \
  -e IMA_MCP_HOST=0.0.0.0 \
  -e IMA_MCP_PORT=8000 \
  ima-mcp
```

## 核心模块使用示例

### 知识库模块 (KnowledgeBase)

```python
from ima_mcp.knowledge_base import KnowledgeBase

# 获取知识库列表
kb = KnowledgeBase()
knowledge_bases = kb.list_knowledge_bases(limit=10)
for kb_info in knowledge_bases:
    print(f"{kb_info['kb_name']} ({kb_info['base_type']})")

# 获取知识库详情
detail = kb.get_knowledge_base("knowledge_base_id")
print(f"知识库名称: {detail['name']}")
print(f"描述: {detail['description']}")

# 搜索知识库内容
results = kb.search_knowledge("knowledge_base_id", "Python 编程")
for result in results:
    print(f"标题: {result.get('title')}")

# 添加网页到知识库
result = kb.import_urls(
    "knowledge_base_id",
    ["https://example.com/article1", "https://example.com/article2"]
)
print(f"添加结果: {result}")

# 上传文件到知识库
result = kb.upload_file("knowledge_base_id", "/path/to/file.pdf")
print(f"上传结果: {result}")

# 批量添加网页
results = kb.batch_import_urls(
    "knowledge_base_id",
    ["https://example.com/article1", "https://example.com/article2", "https://example.com/article3"]
)
for result in results:
    print(f"URLs: {result['urls']}, Success: {result['success']}")

# 批量上传文件
results = kb.batch_upload_files(
    "knowledge_base_id",
    ["/path/to/file1.pdf", "/path/to/file2.md"]
)
for result in results:
    print(f"File: {result['file_path']}, Success: {result['success']}")

# 批量搜索
results = kb.batch_search_knowledge(
    "knowledge_base_id",
    ["Python", "JavaScript", "Java"]
)
for result in results:
    print(f"Query: {result['query']}, Success: {result['success']}, Results: {len(result.get('result', []))}")
```

### 笔记模块 (Notes)

```python
from ima_mcp.notes import Notes

# 搜索笔记
notes = Notes()
results = notes.search_notes("会议纪要")
for result in results:
    print(f"标题: {result.get('doc', {}).get('basic_info', {}).get('title')}")

# 创建笔记
result = notes.create_note("测试笔记", "这是测试笔记的内容")
doc_id = result.get('doc_id')
print(f"创建的笔记 ID: {doc_id}")

# 追加内容到笔记
result = notes.append_note("note_id", "这是追加的内容")
print(f"追加结果: {result}")

# 获取笔记内容
content = notes.get_note("note_id")
print(f"笔记内容: {content.get('content')}")
```

### 客户端模块 (IMAClient)

```python
from ima_mcp.client import IMAClient

# 检查凭证
client = IMAClient()
result = client.check_credentials()
print(f"凭证是否有效: {result['valid']}")
print(f"消息: {result['message']}")
```

## MCP 工具

### 知识库工具

- `list_knowledge_bases`：获取知识库列表
- `get_knowledge_base`：获取知识库详情
- `search_knowledge`：搜索知识库内容
- `import_urls`：添加网页到知识库
- `upload_file`：上传文件到知识库
- `batch_import_urls`：批量添加网页
- `batch_upload_files`：批量上传文件
- `batch_search_knowledge`：批量搜索知识库

### 笔记工具

- `search_notes`：搜索笔记
- `create_note`：创建笔记
- `append_note`：追加内容到笔记
- `get_note`：获取笔记内容

### 通用工具

- `check_credentials`：检查凭证有效性

## 环境变量配置

| 变量名 | 默认值 | 说明 |
|---------|---------|-----|
| `IMA_OPENAPI_CLIENTID` | - | IMA OpenAPI Client ID |
| `IMA_OPENAPI_APIKEY` | - | IMA OpenAPI API Key |
| `IMA_MCP_MODE` | `stdio` | 运行模式，可选值：`stdio` 或 `http` |
| `IMA_MCP_HOST` | `0.0.0.0` | HTTP 服务器监听地址（仅 http 模式） |
| `IMA_MCP_PORT` | `8000` | HTTP 服务器监听端口（仅 http 模式） |

## 错误处理

服务会抛出以下类型的异常：

- `ValueError`：凭证无效或缺少必要参数
- `Exception`：API 请求失败或其他错误

**异常处理示例**：
```python
try:
    kb = KnowledgeBase()
    results = kb.list_knowledge_bases()
except ValueError as e:
    print(f"凭证错误: {e}")
except Exception as e:
    print(f"API 错误: {e}")
```

## 缓存机制

服务内置了缓存机制，提高频繁操作的响应速度：

- **缓存类型**：内存缓存 + 文件缓存
- **缓存过期时间**：1小时
- **最大缓存条目**：100
- **缓存键**：
  - 知识库列表：`knowledge_bases_{limit}`
  - 知识库详情：`knowledge_base_{knowledge_base_id}`

## 最佳实践

1. **凭证管理**：使用环境变量或配置文件存储凭证，避免硬编码
2. **错误处理**：始终捕获并处理可能的异常
3. **批量操作**：对于多个操作，使用批量方法提高效率
4. **缓存利用**：频繁访问的资源会自动缓存，提高响应速度
5. **参数验证**：在调用 API 前验证参数的有效性
6. **部署选择**：本地开发使用 stdio 模式，生产环境使用 Docker + http 模式

## 常见问题

### 凭证错误

**问题**：`缺少 IMA 凭证，请配置 Client ID 和 API Key`
**解决**：确保已正确配置 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 环境变量，或在 `~/.config/ima/` 目录下创建 `client_id` 和 `api_key` 文件

### API 调用失败

**问题**：`API 请求失败: 401 Client Error: Unauthorized for url`
**解决**：检查凭证是否正确，确保 API Key 未过期

### 文件上传失败

**问题**：`文件未上传，请上传后重试`
**解决**：确保文件存在且可读，检查 COS 上传配置

### HTTP 服务启动失败

**问题**：端口被占用
**解决**：使用 `IMA_MCP_PORT` 环境变量指定其他端口

## 开发

```bash
# 安装开发依赖
pip install -e .

# 运行测试
python -m pytest tests/

# 测试 stdio 模式
ima-mcp

# 测试 http 模式
IMA_MCP_MODE=http ima-mcp
```

## 版本历史

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
