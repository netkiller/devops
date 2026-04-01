# Git Merge Tools

git merge 工作流管理工具，用于简化多分支管理、批量合并、流水线合并等操作。

## 安装依赖

需要安装 netkiller 库：

```bash
pip3 install netkiller-devops
```

## 命令行参数

   neo@MacBook-Pro-M2 ~/w/G/devops (master)> merge
    Netkiller git merge tools
    Usage: merge [options] <parameter>

    Options:
    -h, --help            show this help message and exit
    -w ~/workspace, --workspace=~/workspace
                            workspace ~/workspace
    -p PROJECT, --project=PROJECT
                            project directory
    -l /tmp/merge.log, --logfile=/tmp/merge.log
                            log file
    -d, --debug           debug

    Repository:
        -c https://git.netkiller.cn | git@git.netkiller.cn:exmaple.git, --clone=https://git.netkiller.cn | git@git.netkiller.cn:exmaple.git
                            clone branch
        -r 8547cb94, --reset=8547cb94
                            Reset current HEAD to the specified state
        -b master, --checkout=master
                            checkout branch

    Custom merge branch:
        -s development, --source=development
                            source
        -t testing, --to=testing
                            target

    Workflow merge development -> testing -> staging -> production(master):
        --testing           from development to testing
        --staging           from testing to staging
        --production        from staging to production(master)

    Create branch:
        -B mybranch, --branch=mybranch
                            create custom branch
        -f feature/0001, --feature=feature/0001
                            feature branch from development
        -H hotfix/0001, --hotfix=hotfix/0001
                            hotfix branch from master

    Homepage: http://www.netkiller.cn       Author: Neo <netkiller@msn.com>
    Help https://github.com/netkiller/devops/blob/master/doc/merge.md



## 基本用法

```bash
merge [options] <parameter>
```

合并 dev 到 test 分支

    neo@MacBook-Pro-M2 devops % merge -s dev -t test

## 命令行选项

### 通用选项

| 选项 | 说明 |
|------|------|
| `-w DIR` | 工作空间目录（默认 ~/workspace） |
| `-p DIR` | 项目目录 |
| `-C DATE` | 显示指定日期之后的变更记录 |
| `-l FILE` | 日志文件（默认 /tmp/merge.log） |
| `-d` | 调试模式 |

### 仓库操作

| 选项 | 说明 |
|------|------|
| `-c URL` | 克隆仓库 |
| `-r` | 重置当前 HEAD 到指定状态 |
| `-b BRANCH` | 切换到指定分支 |
| `-P` | 推送到远程仓库 |

### 自定义分支合并

| 选项 | 说明 |
|------|------|
| `-s BRANCH` | 源分支 |
| `-t BRANCH` | 目标分支 |

### 流水线合并

| 选项 | 说明 |
|------|------|
| `--pipeline` | 定义合并流水线，如 dev-test-prod |

### 标准工作流

| 选项 | 说明 |
|------|------|
| `--testing` | development → testing |
| `--staging` | testing → staging |
| `--production` | staging → master |

### 分支创建

| 选项 | 说明 |
|------|------|
| `-B BRANCH` | 创建自定义分支 |
| `-f NAME` | 从 development 创建 feature 分支 |
| `-H NAME` | 从 master 创建 hotfix 分支 |

### Cherry-pick

| 选项 | 说明 |
|------|------|
| `--cherry-pick COMMITS` | Cherry-pick 提交（需配合 --pipeline） |

---

## 使用示例

### 基本合并

```bash
# 合并 dev 到 test 分支
merge -s dev -t test
```

### 标准工作流

```bash
# development -> testing
merge --testing

# testing -> staging
merge --staging

# staging -> master
merge --production
```

### 流水线合并

```bash
# 定义多步流水线，一次性执行
merge --pipeline dev-test-prod
```

输出示例：
```
dev -> test -> prod
-------------------- ['dev', 'test'] --------------------
-------------------- ['test', 'prod'] --------------------
```

### 创建分支

```bash
# 创建自定义分支
merge -B mybranch

# 从 master 创建 hotfix 分支
merge -H hotfix/0001

# 从 development 创建 feature 分支
merge -f feature/0001
```

### 仓库操作

```bash
# 克隆仓库
merge -c https://git.netkiller.cn/example.git

# 切换分支
merge -b master

# 强制重置
merge -r
```

### 查看变更记录

```bash
# 查看指定日期后的变更
merge -C "2023-03-01"
```

### Cherry-pick

```bash
# 将提交合并到流水线的每个分支
merge --cherry-pick 9f308d2c --pipeline dev-test-prod
```

---

## 工作流程

### 标准发布流程

```
development → testing → staging → master (production)
```

使用 `--testing`、`--staging`、`--production` 逐步推进，或使用 `--pipeline` 一步完成。

### 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|----------|----------|------|
| Feature | feature/名称 | feature/0001 |
| Hotfix | hotfix/名称 | hotfix/0001 |
| 自定义 | 自定义 | mybranch |

### 合并操作流程

1. 获取远程最新代码
2. 切换到源分支并拉取
3. 切换到目标分支并拉取
4. 执行合并（--no-ff）
5. 推送到远程

---

## 日志

默认日志文件：`/tmp/merge.log`

调试模式输出到标准输出，查看详细执行过程：

```bash
merge -d -s dev -t test
```

---

## 注意事项

1. **工作目录** - 默认使用当前目录，通过 `-p` 或 `-w` 指定项目/工作空间
2. **远程推送** - 合并操作会自动推送到远程目标分支
3. **流水线依赖** - `--cherry-pick` 必须配合 `--pipeline` 使用
4. **冲突处理** - 如遇冲突需手动解决后重新执行
