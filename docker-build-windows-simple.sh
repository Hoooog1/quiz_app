#!/bin/bash
# 简化的 Docker 打包方案
# 注意：PyInstaller 不支持跨平台打包，此方案仅供参考

echo "=========================================="
echo "Docker 打包 Windows 应用（实验性）"
echo "=========================================="

echo ""
echo "⚠️  重要提示："
echo "PyInstaller 不支持跨平台打包！"
echo "在 Linux/macOS 上无法直接生成 Windows .exe 文件"
echo ""
echo "推荐方案："
echo "1. 使用 GitHub Actions（.github/workflows/build.yml）"
echo "2. 使用 Windows 虚拟机"
echo "3. 在真实的 Windows 电脑上运行 build_windows.bat"
echo ""
echo "=========================================="
echo ""

read -p "是否继续尝试？（可能会失败）[y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到 Docker"
    exit 1
fi

# 使用一个简单的 Python 容器来演示
echo "构建 Docker 镜像..."
docker build -f Dockerfile.windows -t quiz-app-builder . 2>&1 | tail -5

echo ""
echo "由于 PyInstaller 的限制，无法在 Linux 容器中生成 Windows 可执行文件"
echo "请使用其他方案"

