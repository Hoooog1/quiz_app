@echo off
chcp 65001 >nul
REM Windows 环境快速设置脚本

echo ==========================================
echo 答题软件 - Windows 环境设置
echo ==========================================
echo.

REM 检查 Python
echo [1/3] 检查 Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 未安装或未添加到 PATH
    echo.
    echo 请执行以下步骤：
    echo 1. 下载 Python: https://www.python.org/downloads/windows/
    echo 2. 安装时勾选 "Add Python to PATH"
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python 已安装
echo.

REM 安装依赖
echo [2/3] 安装 Python 依赖...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

REM 安装 PyInstaller
echo [3/3] 安装 PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PyInstaller 安装失败
    pause
    exit /b 1
)
echo ✅ PyInstaller 安装完成
echo.

echo ==========================================
echo ✅ 环境设置完成！
echo ==========================================
echo.
echo 现在可以运行以下命令来打包应用：
echo   build_windows.bat
echo.
echo 或者手动运行：
echo   python -m PyInstaller --name="简易答题软件" --windowed --onefile ...
echo.
pause

