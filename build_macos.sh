#!/bin/bash
# macOS 打包脚本

echo "=========================================="
echo "开始打包 macOS 应用..."
echo "=========================================="

# 检查是否安装了 PyInstaller
if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "正在安装 PyInstaller..."
    python3 -m pip install pyinstaller
fi

# 检查示例文件是否存在
if [ ! -f "example_questions.xlsx" ]; then
    echo "⚠️  警告: example_questions.xlsx 不存在，将不包含在打包中"
fi
if [ ! -f "example_questions.json" ]; then
    echo "⚠️  警告: example_questions.json 不存在，将不包含在打包中"
fi

# 清理之前的构建
echo "清理之前的构建文件..."
rm -rf build dist *.spec

# 打包应用
echo "开始打包..."
python3 -m PyInstaller --name="简易答题软件" \
    --windowed \
    --onedir \
    --add-data="example_questions.xlsx:." \
    --add-data="example_questions.json:." \
    --hidden-import=PySide6.QtCore \
    --hidden-import=PySide6.QtGui \
    --hidden-import=PySide6.QtWidgets \
    --hidden-import=openpyxl \
    --hidden-import=openpyxl.cell._writer \
    --collect-all=openpyxl \
    --noconfirm \
    main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ macOS 应用打包成功！"
    echo "=========================================="
    echo "应用位置: dist/简易答题软件.app"
    echo ""
    echo "使用提示："
    echo "1. 首次运行可能需要右键点击应用，选择'打开'来绕过 macOS 安全限制"
    echo "2. 可以将应用拖拽到'应用程序'文件夹中"
    echo "3. 应用大小约为 100-200MB（包含所有依赖）"
    echo "4. 注意：这是目录模式（.app bundle），不是单个文件"
else
    echo ""
    echo "❌ 打包失败，请检查错误信息"
    exit 1
fi

