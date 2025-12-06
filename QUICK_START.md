# GitHub Actions 快速开始

## 3 步完成打包

### 步骤 1：创建 GitHub 仓库并推送代码

```bash
cd /Users/user/quiz_app

# 初始化 Git（如果还没有）
git init
git add .
git commit -m "Initial commit: 答题软件"

# 在 GitHub 上创建新仓库，然后：
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 步骤 2：触发打包

1. 打开 GitHub 仓库页面
2. 点击 **"Actions"** 标签
3. 选择 **"Build Executables"** 工作流
4. 点击 **"Run workflow"** 按钮
5. 选择分支（通常是 `main`）
6. 点击 **"Run workflow"**

### 步骤 3：下载文件

1. 等待 10-15 分钟（打包需要时间）
2. 在 Actions 页面找到完成的 workflow
3. 滚动到底部，点击 **"Artifacts"**
4. 下载：
   - `windows-executable` - Windows .exe 文件
   - `macos-executable` - macOS .app 和 .dmg 文件

## 完成！

现在你有了两个平台的可执行文件，可以直接分发给用户使用。

## 详细说明

查看 `GITHUB_ACTIONS_GUIDE.md` 获取更多信息。

