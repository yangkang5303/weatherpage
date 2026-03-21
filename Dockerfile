# 使用 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 Flask
RUN pip install flask

# 复制文件
COPY . .

# 暴露端口
EXPOSE 8080

# 启动 Flask 应用
CMD ["python", "server.py"]
