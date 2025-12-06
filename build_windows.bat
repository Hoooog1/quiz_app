@echo off
chcp 65001 >nul
REM Windows 打包脚本

echo ==========================================
echo 开始打包 Windows 应用...
echo ==========================================

REM 检查是否安装了 PyInstaller
python -m PyInstaller --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 正在安装 PyInstaller...
    python -m pip install pyinstaller
)

REM 检查示例文件是否存在
if not exist "example_questions.xlsx" (
    echo ⚠️  警告: example_questions.xlsx 不存在，将不包含在打包中
)
if not exist "example_questions.json" (
    echo ⚠️  警告: example_questions.json 不存在，将不包含在打包中
)

REM 清理之前的构建
echo 清理之前的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

REM 打包应用
echo 开始打包...
python -m PyInstaller --name="简易答题软件" ^
    --windowed ^
    --onefile ^
    --add-data="example_questions.xlsx;." ^
    --add-data="example_questions.json;." ^
    --hidden-import=PySide6.QtCore ^
    --hidden-import=PySide6.QtGui ^
    --hidden-import=PySide6.QtWidgets ^
    --hidden-import=openpyxl ^
    --hidden-import=openpyxl.cell._writer ^
    --collect-all=openpyxl ^
    --noconfirm ^
    main.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo ✅ Windows 应用打包成功！
    echo ==========================================
    echo 可执行文件位置: dist\简易答题软件.exe
    echo.
    echo 使用提示：
    echo 1. 可以将 exe 文件复制到任何 Windows 电脑上运行（无需安装 Python）
    echo 2. 首次运行可能会被 Windows Defender 拦截，需要点击"更多信息"然后"仍要运行"
    echo 3. 应用大小约为 100-200MB（包含所有依赖）
) else (
    echo.
    echo ❌ 打包失败，请检查错误信息
    exit /b 1
)

