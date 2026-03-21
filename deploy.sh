#!/bin/bash

# Weather App Docker Deployment Script

echo "=== Weather App Deployment ==="

# 0. 确保 weather_data.json 是文件而非目录
if [ -d "./weather_data.json" ]; then
    echo "[0/4] Fixing weather_data.json (was a directory, converting to file)..."
    rm -rf ./weather_data.json
fi
if [ ! -f "./weather_data.json" ]; then
    echo '{"favoriteCities":[],"defaultCapitals":[]}' > ./weather_data.json
fi

# 1. 停止并删除旧容器
echo "[1/4] Stopping and removing existing containers..."
docker compose down --remove-orphans

# 2. 构建 Docker 镜像
echo "[2/4] Building Docker image..."
docker compose build

# 3. 启动容器
echo "[3/4] Starting container..."
docker compose up -d

# 4. 检查状态
echo "[4/4] Checking status..."
docker compose ps

echo ""
echo "=== Deployment Complete ==="
echo "Weather app is running at: http://localhost:8080"
echo ""
echo "Useful commands:"
echo "  docker compose logs -f    # 查看日志"
echo "  docker compose restart   # 重启服务"
echo "  docker compose down      # 停止服务"
