#!/bin/bash
# Docker 容器内使用的 Windows 打包脚本

echo "=========================================="
echo "在 Docker 容器中打包 Windows 应用..."
echo "=========================================="

# 清理之前的构建
rm -rf build dist *.spec

# 打包应用（在 Linux 环境中，但目标是 Windows）
python3 -m PyInstaller --name="简易答题软件" \
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
    main.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Windows 应用打包成功！"
    echo "=========================================="
    echo "可执行文件位置: dist/简易答题软件"
    echo ""
    ls -lh dist/
else
    echo ""
    echo "❌ 打包失败，请检查错误信息"
    exit 1
fi

