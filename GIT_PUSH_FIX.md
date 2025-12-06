# Git 推送问题修复

## 问题
本地分支是 `master`，但尝试推送到 `main` 分支。

## 解决方案

### 方案 1：重命名本地分支为 main（推荐）

```bash
cd /Users/user/quiz_app

# 重命名本地分支
git branch -m master main

# 推送到 GitHub
git push -u origin main
```

### 方案 2：直接推送 master 分支

```bash
cd /Users/user/quiz_app

# 直接推送 master 分支
git push -u origin master
```

**注意**：如果 GitHub 仓库默认分支是 `main`，首次推送 master 后，GitHub 会提示你设置默认分支。

## 推荐操作

使用方案 1，将本地分支重命名为 `main`，这样与 GitHub 的默认分支名一致。

