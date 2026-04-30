# 基础镜像
FROM python:3.9-slim

# 工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装项目
RUN pip install -e .

# 环境变量配置
ENV IMA_OPENAPI_CLIENTID=""
ENV IMA_OPENAPI_APIKEY=""
# 默认使用 HTTP 模式
ENV IMA_MCP_MODE="http"
ENV IMA_MCP_HOST="0.0.0.0"
ENV IMA_MCP_PORT="8000"

# 暴露端口
EXPOSE 8000

# 容器启动命令
CMD ["ima-mcp"]
