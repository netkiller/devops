GIT Sync
========

## 简介

gitsync 是一个用于同步多个 Git 仓库的工具脚本。它从 `~/workspace/git.ini` 读取配置，实现以下功能：

- 从 origin 克隆仓库
- 配置多个 remote
- 同步主分支到所有 remote

## 工作流程

1. 读取 `~/workspace/git.ini` 配置文件
2. 遍历每个配置节（section）
3. 根据配置执行相应的 Git 操作

## 配置文件

配置文件位于 `~/workspace/git.ini`，采用 INI 格式。

### 配置项

| 配置项 | 说明 |
|--------|------|
| `origin` | Git 仓库地址（克隆源） |
| `remote` | 远程仓库名称，多个用逗号分隔 |

### 配置示例

```ini
[project1]
origin = git@github.com:username/repo1.git
remote = upstream,gitlab

[project2]
origin = git@gitlab.com:team/repo2.git
remote = github,bitbucket
```

### 路径说明

- 工作目录：`~/workspace/`
- 仓库目录：`~/workspace/{source}/`，其中 `source` 是从 origin URL 中提取的仓库名

## 使用方法

```bash
./bin/gitsync
```

或

```bash
python3 bin/gitsync
```

## 操作逻辑

### 新仓库（不存在）

1. 从 origin 克隆仓库到 `~/workspace/{仓库名}/`
2. 添加配置的 remote

### 已存在仓库

1. 进入仓库目录
2. 执行 `git reset --hard` 重置工作区
3. 执行 `git pull origin` 拉取最新代码
4. 遍历所有非 origin 的 remote，执行 `git push {remote} master`

## 注意事项

- 脚本假设所有仓库的默认分支为 `master`
- 使用 `git pull origin` 直接拉取，不处理冲突
- `git reset --hard` 会丢弃所有未提交的更改
- 需要确保 SSH key 已配置到对应的 Git 服务商
