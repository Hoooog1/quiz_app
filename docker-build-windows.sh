#!/bin/bash
# 在 macOS 上使用 Docker + Wine 打包 Windows 可执行文件

echo "=========================================="
echo "使用 Docker + Wine 打包 Windows 应用"
echo "=========================================="
echo ""
echo "⚠️  注意：此方法使用 Wine 模拟 Windows 环境"
echo "   打包过程较慢，且生成的 .exe 需要在 Windows 上测试"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到 Docker"
    echo "请先安装 Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ 错误: Docker 未运行"
    echo "请启动 Docker Desktop"
    exit 1
fi

echo "✅ Docker 已就绪"
echo ""

# 创建 dist 目录
mkdir -p dist

# 构建 Docker 镜像
echo "正在构建 Docker 镜像（这可能需要几分钟）..."
docker build -f Dockerfile.windows -t quiz-app-windows-builder . 2>&1 | grep -E "(Step|ERROR|Successfully)" || true

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Docker 镜像构建失败"
    exit 1
fi

echo ""
echo "✅ Docker 镜像构建成功"
echo ""

# 运行容器并打包
echo "正在打包 Windows 应用（这可能需要 10-20 分钟）..."
echo "正在下载和安装 Windows Python，请耐心等待..."
docker run --rm \
    -v "$(pwd)/dist:/app/dist" \
    -e DISPLAY=:99 \
    quiz-app-windows-builder

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 打包完成！"
    echo "=========================================="
    if [ -f "dist/简易答题软件.exe" ]; then
        echo "Windows 可执行文件: dist/简易答题软件.exe"
        ls -lh dist/简易答题软件.exe
        echo ""
        echo "⚠️  重要提示："
        echo "1. 请在 Windows 系统上测试生成的 .exe 文件"
        echo "2. 如果无法运行，建议使用 GitHub Actions 或 Windows 虚拟机"
    else
        echo "⚠️  未找到 .exe 文件，请检查错误信息"
    fi
else
    echo ""
    echo "❌ 打包失败"
    echo ""
    echo "如果遇到问题，建议使用："
    echo "1. GitHub Actions（推荐）：.github/workflows/build.yml"
    echo "2. Windows 虚拟机"
    exit 1
fi

