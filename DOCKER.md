# IMA MCP Docker 部署指南

## 环境要求

- Docker
- Docker Compose

## 配置步骤

### 1. 配置环境变量

复制环境变量示例文件并填写实际的 IMA OpenAPI 凭证：

```bash
cp .env.example .env
# 编辑 .env 文件，填写您的 IMA OpenAPI 凭证
```

### 2. 构建 Docker 镜像

使用 Docker Compose 构建镜像：

```bash
docker-compose build
```

### 3. 运行容器

启动 Docker 容器：

```bash
docker-compose up -d
```

### 4. 进入容器

进入运行中的容器：

```bash
docker exec -it ima-mcp bash
```

## 构建方式

### 直接使用 Docker 命令

```bash
# 构建镜像
docker build -t ima-mcp .

# 运行容器
docker run -it --name ima-mcp \
  -e IMA_OPENAPI_CLIENTID=your_client_id \
  -e IMA_OPENAPI_APIKEY=your_api_key \
  -v $(pwd):/app \
  ima-mcp
```

## 注意事项

1. **凭证安全**：请确保不要将包含真实凭证的 `.env` 文件提交到版本控制
2. **网络连接**：容器需要能够访问 IMA OpenAPI 服务
3. **文件权限**：如果需要上传文件到容器，确保相关目录有正确的权限

## 常见问题

### 构建失败
- 检查网络连接是否正常
- 确保 Docker 服务正在运行

### 凭证错误
- 检查 `.env` 文件中的凭证是否正确
- 确保 IMA OpenAPI 凭证未过期

### 容器启动失败
- 查看容器日志：`docker logs ima-mcp`
- 检查端口是否被占用（如果启用了端口映射）
