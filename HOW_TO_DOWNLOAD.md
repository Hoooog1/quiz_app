# 如何下载打包好的文件

## 步骤详解

### 步骤 1：进入 GitHub Actions 页面

1. 打开你的 GitHub 仓库：https://github.com/Hoooog1/quiz_app
2. 点击顶部的 **"Actions"** 标签

### 步骤 2：找到完成的 Workflow

1. 在左侧工作流列表中找到 **"Build Executables"**
2. 点击它
3. 你会看到所有运行记录
4. 找到状态为 **绿色勾号 ✅** 的最近一次运行（表示成功）
5. 点击这次运行

### 步骤 3：下载 Artifacts（打包好的文件）

1. 在 workflow run 页面中，向下滚动
2. 找到 **"Artifacts"** 部分（通常在页面底部）
3. 你会看到两个可下载的文件：
   - **windows-executable** - Windows 可执行文件
   - **macos-executable** - macOS 应用文件

4. 点击你想要下载的 Artifact
5. 文件会自动下载为 ZIP 压缩包

### 步骤 4：解压文件

下载后：

**Windows 文件：**
- 解压 `windows-executable.zip`
- 里面会有 `简易答题软件.exe` 文件
- 这就是 Windows 可执行文件

**macOS 文件：**
- 解压 `macos-executable.zip`
- 里面会有：
  - `简易答题软件.app` - macOS 应用
  - `简易答题软件.dmg` - macOS 安装包（如果有）

## 图示说明

```
GitHub 仓库页面
    ↓
点击 "Actions" 标签
    ↓
选择 "Build Executables" 工作流
    ↓
找到绿色勾号 ✅ 的最近运行
    ↓
点击进入详情页
    ↓
向下滚动到 "Artifacts" 部分
    ↓
点击下载 windows-executable 或 macos-executable
    ↓
解压 ZIP 文件
    ↓
获得可执行文件！
```

## 注意事项

1. **文件保留时间**：Artifacts 会在 GitHub 上保留 30 天，之后自动删除
2. **文件大小**：每个 Artifact 大约 100-200MB（包含所有依赖）
3. **下载速度**：取决于你的网络速度，可能需要几分钟

## 如果找不到 Artifacts

如果看不到 Artifacts 部分，可能的原因：

1. **打包还在进行中**：等待打包完成（通常需要 10-15 分钟）
2. **打包失败了**：检查 workflow 日志，查看错误信息
3. **页面需要刷新**：尝试刷新页面

## 快速检查清单

- ✅ Workflow 状态是绿色勾号（成功）
- ✅ 所有步骤都显示成功
- ✅ 页面底部有 "Artifacts" 部分
- ✅ 可以看到 windows-executable 和 macos-executable

## 使用下载的文件

### Windows

1. 解压 `windows-executable.zip`
2. 找到 `简易答题软件.exe`
3. 双击运行（首次可能被 Windows Defender 拦截，需要点击"更多信息"然后"仍要运行"）

### macOS

1. 解压 `macos-executable.zip`
2. 找到 `简易答题软件.app`
3. 首次运行可能需要右键点击，选择"打开"来绕过 macOS 安全限制
4. 或者使用 `简易答题软件.dmg` 安装包

## 提示

- 可以将文件分享给其他人使用
- 不需要安装 Python 或其他依赖
- 文件是独立的可执行文件

