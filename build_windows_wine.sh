#!/bin/bash
# 在 Wine 环境中打包 Windows 应用

set -e

echo "=========================================="
echo "使用 Wine 打包 Windows 应用"
echo "=========================================="

# 启动虚拟显示（如果还没有）
if ! pgrep -x Xvfb > /dev/null; then
    Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
    sleep 3
fi
export DISPLAY=:99

# Wine 配置
export WINEDLLOVERRIDES="mscoree,mshtml="
export WINEARCH=win64

echo "正在配置 Wine 环境..."

# 确保 Wine 已初始化
if [ ! -d "$HOME/.wine" ]; then
    echo "初始化 Wine..."
    winecfg -v win10 -f 2>&1 | head -5 || true
    sleep 2
fi

# 下载并安装 Windows 版本的 Python（如果还没有）
PYTHON_WIN_DIR="$HOME/.wine/drive_c/Python39"
if [ ! -d "$PYTHON_WIN_DIR" ] || [ ! -f "$PYTHON_WIN_DIR/python.exe" ]; then
    echo "下载 Windows Python 3.9.13..."
    wget -q --show-progress https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe -O /tmp/python.exe || {
        echo "❌ 下载 Python 失败，尝试备用链接..."
        wget -q https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe -O /tmp/python.exe || {
            echo "❌ 无法下载 Python，请检查网络连接"
            exit 1
        }
    }
    
    echo "安装 Windows Python（这可能需要 5-10 分钟）..."
    echo "请耐心等待，Wine 安装 Windows 程序较慢..."
    wine /tmp/python.exe /quiet InstallAllUsers=1 PrependPath=1 2>&1 | tail -10 || {
        echo "⚠️  Python 安装可能未完全成功，继续尝试..."
    }
    sleep 10
    
    # 验证安装
    if [ ! -f "$PYTHON_WIN_DIR/python.exe" ]; then
        echo "❌ Windows Python 安装失败"
        echo "尝试手动安装..."
        wine /tmp/python.exe /passive InstallAllUsers=1 PrependPath=1
        sleep 10
    fi
fi

# 使用 Wine 运行 Windows Python
WINE_PYTHON="wine $PYTHON_WIN_DIR/python.exe"

echo "检查 Windows Python..."
$WINE_PYTHON --version 2>&1 || {
    echo "❌ Windows Python 未正确安装或无法运行"
    echo "Wine 环境可能有问题，建议使用其他打包方案"
    exit 1
}

echo "✅ Windows Python 已就绪"
echo ""

echo "安装 Windows 版本的依赖（这可能需要几分钟）..."
$WINE_PYTHON -m pip install --upgrade pip 2>&1 | tail -3
$WINE_PYTHON -m pip install -r requirements.txt 2>&1 | tail -5
$WINE_PYTHON -m pip install pyinstaller 2>&1 | tail -3

echo ""
echo "开始打包 Windows 应用..."

# 清理
rm -rf build dist *.spec

# 使用 Wine 运行 PyInstaller
$WINE_PYTHON -m PyInstaller --name="简易答题软件" \
    --windowed \
    --onefile \
    --add-data="example_questions.xlsx;." \
    --add-data="example_questions.json;." \
    --hidden-import=PySide6.QtCore \
    --hidden-import=PySide6.QtGui \
    --hidden-import=PySide6.QtWidgets \
    --hidden-import=openpyxl \
    --hidden-import=openpyxl.cell._writer \
    --collect-all=openpyxl \
    --noconfirm \
    main.py 2>&1 | tail -20

if [ $? -eq 0 ] && [ -f "dist/简易答题软件.exe" ]; then
    echo ""
    echo "=========================================="
    echo "✅ Windows 应用打包成功！"
    echo "=========================================="
    echo "可执行文件: dist/简易答题软件.exe"
    ls -lh dist/简易答题软件.exe
else
    echo ""
    echo "❌ 打包失败或文件未生成"
    echo ""
    echo "如果持续失败，建议使用："
    echo "1. GitHub Actions（推荐）"
    echo "2. Windows 虚拟机"
    exit 1
fi

