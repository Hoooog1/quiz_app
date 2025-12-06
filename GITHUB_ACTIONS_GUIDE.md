# GitHub Actions 打包指南

使用 GitHub Actions 可以自动在 Windows 和 macOS 环境中打包应用，无需本地安装虚拟机或 Docker。

## 快速开始

### 步骤 1：创建 GitHub 仓库

1. 登录 GitHub：https://github.com
2. 点击右上角的 "+" → "New repository"
3. 填写仓库名称（如 `quiz-app`）
4. 选择 "Public" 或 "Private"
5. 点击 "Create repository"

### 步骤 2：推送代码到 GitHub

在项目目录中运行：

```bash
cd /Users/user/quiz_app

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 答题软件"

# 添加远程仓库（替换 YOUR_USERNAME 和 YOUR_REPO）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送到 GitHub
git push -u origin main
```

**注意**：如果仓库使用 `master` 分支，将 `main` 改为 `master`

### 步骤 3：触发 GitHub Actions

有两种方式触发打包：

#### 方式 1：手动触发（推荐）

1. 进入 GitHub 仓库页面
2. 点击 "Actions" 标签
3. 在左侧选择 "Build Executables"
4. 点击 "Run workflow" 按钮
5. 选择分支（通常是 `main`）
6. 点击 "Run workflow"

#### 方式 2：自动触发

- 推送代码到 `main` 或 `master` 分支时会自动触发
- 创建版本标签（如 `v1.0.0`）时会自动触发

### 步骤 4：下载打包好的文件

1. 等待打包完成（通常需要 5-10 分钟）
2. 在 Actions 页面找到完成的 workflow run
3. 滚动到底部，找到 "Artifacts" 部分
4. 下载：
   - `windows-executable` - Windows 可执行文件
   - `macos-executable` - macOS 应用和 DMG 文件

## 详细说明

### 工作流配置

GitHub Actions 工作流文件位于：`.github/workflows/build.yml`

这个工作流会：
1. 在 Windows 环境中打包 Windows .exe 文件
2. 在 macOS 环境中打包 macOS .app 文件
3. 自动上传打包好的文件作为 Artifacts

### 触发条件

工作流会在以下情况自动触发：
- 推送到 `main` 或 `master` 分支
- 创建版本标签（如 `v1.0.0`）
- 手动触发（在 Actions 页面）

### 打包时间

- **Windows 打包**：约 3-5 分钟
- **macOS 打包**：约 5-8 分钟
- **总计**：约 8-13 分钟

### 文件保留

打包好的文件会在 GitHub 上保留 30 天，之后自动删除。

## 常见问题

### Q: 如何查看打包进度？

A: 
1. 进入仓库的 "Actions" 标签
2. 点击正在运行的 workflow
3. 可以看到实时的构建日志

### Q: 打包失败怎么办？

A:
1. 查看 Actions 页面的错误信息
2. 检查代码是否有语法错误
3. 确保所有依赖都在 `requirements.txt` 中
4. 检查是否有文件缺失（如示例文件）

### Q: 如何只打包一个平台？

A: 编辑 `.github/workflows/build.yml`，注释掉不需要的 job：

```yaml
# 只打包 Windows
# build-macos:
#   ...

# 只打包 macOS
# build-windows:
#   ...
```

### Q: 如何修改打包配置？

A: 编辑 `.github/workflows/build.yml` 文件中的 PyInstaller 参数。

### Q: 打包的文件在哪里？

A: 在 Actions 页面，每个完成的 workflow run 底部有 "Artifacts" 部分，可以下载。

### Q: 可以自动发布到 Releases 吗？

A: 可以！编辑工作流，添加发布步骤。示例：

```yaml
- name: Create Release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: ${{ github.ref }}
    release_name: Release ${{ github.ref }}
    draft: false
    prerelease: false
```

## 高级用法

### 使用版本标签触发

创建版本标签来触发打包：

```bash
# 创建标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0
```

### 自定义打包参数

编辑 `.github/workflows/build.yml`，修改 PyInstaller 参数：

```yaml
python -m PyInstaller --name="你的应用名" \
    --windowed \
    --onefile \
    # 添加你的自定义参数
```

### 添加图标

1. 准备图标文件：
   - Windows: `.ico` 格式
   - macOS: `.icns` 格式
2. 添加到仓库
3. 在 PyInstaller 命令中添加 `--icon=icon.ico`

## 优势

使用 GitHub Actions 的优势：

✅ **完全自动化** - 无需手动操作  
✅ **跨平台** - 同时打包 Windows 和 macOS  
✅ **无需本地环境** - 不需要虚拟机或 Docker  
✅ **免费** - GitHub 提供免费的 Actions 额度  
✅ **可重复** - 每次打包环境一致  
✅ **版本控制** - 打包历史可追溯  

## 限制

- 免费账户每月有使用时间限制（通常足够使用）
- 需要将代码推送到 GitHub（公开或私有仓库都可以）
- 首次设置需要几分钟

## 下一步

1. 按照上面的步骤设置 GitHub Actions
2. 推送代码到 GitHub
3. 触发打包
4. 下载打包好的文件
5. 测试应用

如果遇到问题，可以查看 GitHub Actions 的日志来诊断问题。

