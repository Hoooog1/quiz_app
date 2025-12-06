# 使用 Windows 虚拟机打包指南

本指南将帮助你在 macOS 上使用 Windows 虚拟机来打包 Windows 可执行文件。

## 准备工作

### 1. 选择虚拟机软件

推荐以下虚拟机软件（按推荐顺序）：

1. **Parallels Desktop**（付费，性能最好）
   - 下载：https://www.parallels.com/products/desktop/
   - 优点：性能最佳，与 macOS 集成最好
   - 缺点：需要付费

2. **VMware Fusion**（付费，性能好）
   - 下载：https://www.vmware.com/products/fusion.html
   - 优点：性能好，功能强大
   - 缺点：需要付费

3. **VirtualBox**（免费，性能一般）
   - 下载：https://www.virtualbox.org/
   - 优点：完全免费
   - 缺点：性能较慢，但足够使用

### 2. 准备 Windows 系统

你需要一个 Windows 10/11 的 ISO 镜像文件：

- **Windows 11**（推荐）：https://www.microsoft.com/software-download/windows11
- **Windows 10**：https://www.microsoft.com/software-download/windows10

## 虚拟机设置步骤

### 步骤 1：创建虚拟机

#### Parallels Desktop
1. 打开 Parallels Desktop
2. 点击"文件" → "新建"
3. 选择"安装 Windows"或"使用 ISO 镜像"
4. 选择下载的 Windows ISO 文件
5. 按照向导完成安装

#### VMware Fusion
1. 打开 VMware Fusion
2. 点击"文件" → "新建"
3. 选择"从光盘或镜像安装"
4. 选择 Windows ISO 文件
5. 按照向导完成安装

#### VirtualBox
1. 打开 VirtualBox
2. 点击"新建"
3. 设置虚拟机名称和类型（Windows 10/11）
4. 分配内存（建议至少 4GB）
5. 创建虚拟硬盘（建议至少 50GB）
6. 在设置中挂载 Windows ISO 文件
7. 启动虚拟机并安装 Windows

### 步骤 2：安装 Windows

1. 启动虚拟机
2. 按照 Windows 安装向导完成安装
3. 安装完成后，安装虚拟机工具（增强功能）：
   - **Parallels**: 自动安装 Parallels Tools
   - **VMware**: 自动安装 VMware Tools
   - **VirtualBox**: 菜单 → 设备 → 安装增强功能

### 步骤 3：在 Windows 中设置环境

#### 3.1 安装 Python

1. 下载 Python 3.9 或更高版本：
   - https://www.python.org/downloads/windows/
2. 运行安装程序
3. **重要**：勾选"Add Python to PATH"
4. 完成安装

#### 3.2 复制项目文件

将项目文件复制到 Windows 虚拟机中：

**方法 1：共享文件夹（推荐）**
- **Parallels**: 自动启用共享文件夹，在 Windows 中访问 `\\Mac\Home`
- **VMware**: 启用共享文件夹功能
- **VirtualBox**: 设置共享文件夹

**方法 2：使用 U 盘**
- 将项目文件复制到 U 盘
- 在虚拟机中访问 U 盘

**方法 3：使用网络传输**
- 在 macOS 上启动简单的 HTTP 服务器
- 在 Windows 中下载文件

#### 3.3 在 Windows 中安装依赖

1. 打开命令提示符（CMD）或 PowerShell
2. 进入项目目录
3. 运行：

```batch
pip install -r requirements.txt
```

#### 3.4 运行打包脚本

在项目目录中运行：

```batch
build_windows.bat
```

或者手动运行：

```batch
python -m PyInstaller --name="简易答题软件" --windowed --onefile --add-data="example_questions.xlsx;." --add-data="example_questions.json;." --hidden-import=openpyxl main.py
```

### 步骤 4：获取打包好的文件

打包完成后，可执行文件位于 `dist\简易答题软件.exe`

将文件复制回 macOS：
- 使用共享文件夹
- 使用 U 盘
- 通过网络传输

## 快速设置脚本

在 Windows 虚拟机中，你可以创建一个快速设置脚本：

### setup_windows.bat

```batch
@echo off
echo ==========================================
echo 答题软件 - Windows 环境设置
echo ==========================================

echo.
echo 1. 检查 Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 未安装，请先安装 Python
    pause
    exit /b 1
)

echo.
echo 2. 安装依赖...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 3. 安装 PyInstaller...
pip install pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PyInstaller 安装失败
    pause
    exit /b 1
)

echo.
echo ✅ 环境设置完成！
echo.
echo 现在可以运行 build_windows.bat 来打包应用
pause
```

## 常见问题

### Q: 虚拟机运行很慢怎么办？
A: 
- 增加分配给虚拟机的内存（至少 4GB）
- 启用硬件加速
- 关闭不必要的 Windows 功能
- 使用 Parallels 或 VMware（性能更好）

### Q: 如何共享文件？
A:
- **Parallels**: 自动共享，在 Windows 中访问 `\\Mac\Home`
- **VMware**: 设置 → 共享文件夹
- **VirtualBox**: 设置 → 共享文件夹

### Q: 打包失败怎么办？
A:
- 确保 Python 已添加到 PATH
- 确保所有依赖都已安装
- 检查错误信息，可能需要安装额外的 Windows 依赖

### Q: 生成的 .exe 文件很大？
A:
- 这是正常的，包含了所有 Python 依赖
- 大小通常在 100-200MB
- 可以使用 UPX 压缩（可选）

## 推荐配置

### 虚拟机配置
- **内存**: 4GB 或更多
- **CPU**: 2 核心或更多
- **硬盘**: 50GB 或更多
- **显示**: 启用 3D 加速（如果支持）

### Windows 配置
- **版本**: Windows 10 或 Windows 11
- **Python**: 3.9 或更高版本
- **磁盘空间**: 至少 10GB 可用空间（用于打包）

## 完成后的清理

打包完成后，你可以：
1. 保存虚拟机快照（方便下次使用）
2. 关闭虚拟机以节省资源
3. 将打包好的 .exe 文件复制到 macOS

## 提示

- 首次设置可能需要 30-60 分钟
- 之后每次打包只需要 5-10 分钟
- 建议保存虚拟机快照，方便重复使用
- 如果经常需要打包，可以考虑使用 GitHub Actions（自动化）

