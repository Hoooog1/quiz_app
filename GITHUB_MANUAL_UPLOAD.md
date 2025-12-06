# GitHub 手动上传文件指南

## 方法 1：通过 GitHub Web 界面上传（最简单）

### 步骤 1：创建仓库（如果还没有）

1. 访问 https://github.com
2. 点击右上角的 "+" → "New repository"
3. 填写仓库名称：`quiz_app`
4. 选择 "Public" 或 "Private"
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 步骤 2：上传文件

1. 进入刚创建的仓库页面
2. 点击 **"uploading an existing file"** 链接（在快速设置区域）
3. 或者点击 **"Add file"** → **"Upload files"**

### 步骤 3：选择文件

**需要上传的文件：**
- ✅ `main.py` - 主程序文件
- ✅ `requirements.txt` - 依赖文件
- ✅ `example_questions.xlsx` - 示例 Excel 文件
- ✅ `example_questions.json` - 示例 JSON 文件
- ✅ `README.md` - 说明文档
- ✅ `.github/workflows/build.yml` - GitHub Actions 配置（重要！）

**可选文件：**
- `build_macos.sh` - macOS 打包脚本
- `build_windows.bat` - Windows 打包脚本
- `setup_windows.bat` - Windows 环境设置脚本
- `GITHUB_ACTIONS_GUIDE.md` - 使用指南
- `QUICK_START.md` - 快速开始指南
- `VIRTUAL_MACHINE_GUIDE.md` - 虚拟机指南

### 步骤 4：上传文件夹结构

**重要**：`.github/workflows/build.yml` 文件需要放在正确的文件夹结构中。

上传步骤：
1. 先上传普通文件（main.py, requirements.txt 等）
2. 然后创建 `.github` 文件夹：
   - 点击 "Add file" → "Create new file"
   - 输入路径：`.github/workflows/build.yml`
   - 复制 `build.yml` 的内容粘贴进去
   - 点击 "Commit new file"

### 步骤 5：提交文件

1. 在页面底部填写提交信息（如："Initial commit"）
2. 选择 "Commit directly to the main branch"
3. 点击 "Commit changes" 或 "Commit new file"

## 方法 2：使用 GitHub Desktop（图形界面）

### 步骤 1：下载 GitHub Desktop

1. 访问：https://desktop.github.com/
2. 下载并安装 GitHub Desktop

### 步骤 2：克隆仓库

1. 打开 GitHub Desktop
2. 点击 "File" → "Clone repository"
3. 选择你的仓库
4. 选择本地保存位置
5. 点击 "Clone"

### 步骤 3：复制文件

1. 将项目文件复制到克隆的文件夹中
2. 在 GitHub Desktop 中会看到文件变更
3. 填写提交信息
4. 点击 "Commit to main"
5. 点击 "Push origin" 推送到 GitHub

## 方法 3：使用 ZIP 上传（临时方案）

如果文件很多，可以：

1. 在本地将项目打包成 ZIP
2. 在 GitHub 上创建仓库
3. 使用 GitHub CLI 或其他工具上传

## 重要提示

### 必须上传的文件

这些文件是必需的：
- ✅ `main.py`
- ✅ `requirements.txt`
- ✅ `.github/workflows/build.yml`（用于自动打包）

### 文件夹结构

确保 `.github/workflows/build.yml` 的路径正确：
```
quiz_app/
├── main.py
├── requirements.txt
├── README.md
├── example_questions.xlsx
├── example_questions.json
└── .github/
    └── workflows/
        └── build.yml  ← 这个文件很重要！
```

### 创建 .github 文件夹的技巧

由于 `.github` 是隐藏文件夹（以点开头），在 Web 界面创建时：

1. 点击 "Add file" → "Create new file"
2. 在文件名输入框中输入：`.github/workflows/build.yml`
3. GitHub 会自动创建文件夹结构
4. 粘贴 `build.yml` 的内容
5. 提交文件

## 验证上传

上传完成后：

1. 检查仓库页面，确认所有文件都在
2. 确认 `.github/workflows/build.yml` 文件存在
3. 点击 "Actions" 标签，应该能看到 "Build Executables" 工作流

## 下一步

文件上传完成后：

1. 进入仓库的 "Actions" 标签
2. 选择 "Build Executables" 工作流
3. 点击 "Run workflow" 手动触发打包
4. 等待打包完成
5. 下载打包好的文件

## 常见问题

### Q: 如何上传隐藏文件夹（.github）？

A: 使用 "Create new file" 功能，输入完整路径 `.github/workflows/build.yml`，GitHub 会自动创建文件夹。

### Q: 文件太多怎么办？

A: 可以分批上传，或者使用 GitHub Desktop。

### Q: 上传后如何修改文件？

A: 在 GitHub 网页上点击文件，然后点击编辑按钮（铅笔图标）进行修改。

### Q: 可以上传整个文件夹吗？

A: GitHub Web 界面不支持直接上传文件夹，需要逐个上传文件，或使用 GitHub Desktop。

