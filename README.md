# 简易答题软件

一个支持单选题和多选题的跨平台答题软件，可在 macOS 和 Windows 系统上运行。

## 功能特点

- ✅ 支持单选题
- ✅ 支持多选题
- ✅ 题目导入（支持 JSON 和 Excel 格式）
- ✅ 上一题/下一题导航
- ✅ 答案提交和评分
- ✅ 正确答案显示
- ✅ 实时得分统计
- ✅ 现代化的用户界面

## 安装要求

- Python 3.7 或更高版本
- PySide6（通过 requirements.txt 安装）
- openpyxl（用于读取 Excel 文件）
- PyInstaller（用于打包可执行文件，可选）

## 安装步骤

1. 克隆或下载项目到本地

2. 安装依赖：
   - **macOS/Linux**:
     ```bash
     python3 -m pip install -r requirements.txt
     # 或者使用
     pip3 install -r requirements.txt
     ```
   - **Windows**:
     ```bash
     pip install -r requirements.txt
     # 或者使用
     python -m pip install -r requirements.txt
     ```

## 使用方法

1. 运行程序：
   - **macOS/Linux**:
     ```bash
     python3 main.py
     ```
   - **Windows**:
     ```bash
     python main.py
     ```

2. 导入题目：
   - 点击"导入题目"按钮
   - 选择 JSON 或 Excel 格式的题目文件
   - 程序会自动加载题目

3. 答题：
   - 选择答案（单选或多选）
   - 点击"提交答案"查看结果
   - 使用"上一题"和"下一题"按钮导航

## 题目文件格式

程序支持两种文件格式：**JSON** 和 **Excel (.xlsx/.xls)**

### Excel 格式（推荐）

Excel 格式更易于批量编辑题目，推荐使用。

#### Excel 表格结构

| 题目类型 | 题目 | 选项A | 选项B | 选项C | 选项D | 选项E（可选） | 选项F（可选） | 正确答案 |
|---------|------|-------|-------|-------|-------|--------------|--------------|---------|
| single | 题目内容 | 选项1 | 选项2 | 选项3 | 选项4 | - | - | B |
| multiple | 题目内容 | 选项1 | 选项2 | 选项3 | 选项4 | - | - | A,C |

#### Excel 格式说明

1. **第一行为表头**（列名），必须包含以下列：
   - `题目类型` 或 `类型` 或 `Type`
   - `题目` 或 `Question`
   - `选项A`、`选项B`、`选项C`、`选项D`（或 `选项1`、`选项2` 等）
   - `正确答案` 或 `答案` 或 `Answer`

2. **题目类型**：
   - 单选题：填写 `单选` 或 `单选题`（推荐使用中文）
   - 多选题：填写 `多选` 或 `多选题`（推荐使用中文）
   - 也支持英文：`single` 或 `multiple`

3. **选项**：
   - 支持 2-6 个选项
   - 选项列可以是 `选项A`、`选项B` 等，或直接是字母 `A`、`B`、`C`、`D`
   - 空的选项列会被自动忽略

4. **正确答案**：
   - **单选题**：填写选项字母（如 `B`）或数字（如 `2`，从1开始）
   - **多选题**：用逗号分隔，如 `A,C` 或 `1,3`

5. **示例**：
   ```
   题目类型 | 题目 | 选项A | 选项B | 选项C | 选项D | 正确答案
   单选     | Python是什么语言？ | 编译型 | 解释型 | 汇编 | 机器 | B
   多选     | Python的数据结构？ | list | dict | set | array | A,B,C
   ```

### JSON 格式

JSON 格式支持两种结构：

### 格式 1：直接数组
```json
[
  {
    "type": "single",
    "question": "这是题目内容？",
    "options": ["选项A", "选项B", "选项C", "选项D"],
    "answer": 0
  },
  {
    "type": "multiple",
    "question": "这是多选题？（多选）",
    "options": ["选项A", "选项B", "选项C", "选项D"],
    "answer": [0, 2]
  }
]
```

### 格式 2：包含 questions 字段的对象
```json
{
  "questions": [
    {
      "type": "single",
      "question": "这是题目内容？",
      "options": ["选项A", "选项B", "选项C", "选项D"],
      "answer": 0
    }
  ]
}
```

### 字段说明

- `type`: 题目类型
  - `"single"`: 单选题
  - `"multiple"`: 多选题
- `question`: 题目内容（字符串）
- `options`: 选项列表（字符串数组）
- `answer`: 正确答案
  - 单选题：整数，表示选项索引（从 0 开始）
  - 多选题：整数数组，表示选项索引列表

## 示例文件

项目包含两个示例文件：
- `example_questions.json` - JSON 格式示例
- `example_questions.xlsx` - Excel 格式示例

你可以参考这些文件的格式创建自己的题目文件。

## 系统要求

- macOS 10.13 或更高版本
- Windows 10 或更高版本
- Python 3.7+

## 注意事项

- 题目文件必须使用 UTF-8 编码
- 选项数量至少为 2 个
- 多选题的答案必须是数组格式

## 打包为可执行文件

**重要提示**：PyInstaller 不支持跨平台打包
- 在 macOS 上只能打包 macOS 应用（.app）
- 在 Windows 上只能打包 Windows 应用（.exe）
- 如需同时获得两个平台的可执行文件，请使用 GitHub Actions 或虚拟机

如果你想将程序打包成可执行文件，可以直接运行：

### macOS

```bash
# 方式1：使用脚本（推荐）
./build_macos.sh

# 方式2：手动打包
python3 -m pip install pyinstaller
python3 -m PyInstaller --name="简易答题软件" --windowed --onedir \
    --add-data="example_questions.xlsx:." \
    --add-data="example_questions.json:." \
    --hidden-import=openpyxl \
    main.py
```

打包完成后，应用位于 `dist/简易答题软件.app`（这是一个目录，macOS 的 .app bundle 格式）

**macOS 注意事项：**
- 首次运行可能需要右键点击应用，选择"打开"来绕过 macOS 安全限制
- 可以将应用拖拽到"应用程序"文件夹中

### Windows

```batch
REM 方式1：使用脚本（推荐）
build_windows.bat

REM 方式2：手动打包
python -m pip install pyinstaller
python -m PyInstaller --name="简易答题软件" --windowed --onefile ^
    --add-data="example_questions.xlsx;." ^
    --add-data="example_questions.json;." ^
    --hidden-import=openpyxl ^
    main.py
```

打包完成后，可执行文件位于 `dist\简易答题软件.exe`

**Windows 注意事项：**
- 首次运行可能会被 Windows Defender 拦截，需要点击"更多信息"然后"仍要运行"
- 可以将 exe 文件复制到任何 Windows 电脑上运行（无需安装 Python）

### 跨平台打包方案

如果你在 macOS 上，但需要 Windows 可执行文件，可以使用以下方案：

#### 方案 1：GitHub Actions（推荐）

1. 将代码推送到 GitHub
2. 使用提供的 `.github/workflows/build.yml` 工作流
3. 在 GitHub Actions 中自动在 Windows 和 macOS 环境中分别打包
4. 下载打包好的可执行文件

#### 方案 2：使用 Windows 虚拟机（推荐用于本地打包）

在 macOS 上安装 Windows 虚拟机，然后在虚拟机中打包。

**详细步骤请查看：`VIRTUAL_MACHINE_GUIDE.md`**

快速步骤：
1. 安装虚拟机软件（Parallels/VMware/VirtualBox）
2. 安装 Windows 10/11
3. 在 Windows 中安装 Python 和依赖
4. 运行 `setup_windows.bat` 设置环境
5. 运行 `build_windows.bat` 打包应用

#### 方案 3：使用 Docker（不推荐）

**注意**：PyInstaller 不支持跨平台打包，在 Linux 容器中无法直接生成 Windows .exe 文件。

虽然可以创建 Docker 容器，但需要：
- 使用 Wine 运行 Windows 版本的 Python 和 PyInstaller
- 配置复杂，且可能不稳定
- 生成的 .exe 文件可能无法正常运行

**推荐**：使用方案 1（GitHub Actions）或方案 2（虚拟机）

### 打包选项说明

- `--windowed`: 不显示控制台窗口（GUI 应用）
- `--onefile` (Windows): 打包成单个可执行文件
- `--onedir` (macOS): 打包成目录（.app bundle 格式）
- `--add-data`: 包含示例文件
- `--hidden-import`: 确保导入必要的模块

## 许可证

本项目仅供学习和个人使用。

