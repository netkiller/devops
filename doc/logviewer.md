日志查看工具
===========

logviewer 是一组日志查看工具，支持本地日志文件、Docker 容器日志和 Kubernetes Pod 日志的实时查看。采用 TUI 交互界面，方便快捷。

## 安装依赖

三个脚本均依赖以下 Python 库：

```bash
pip install simple_term_menu prompt_toolkit
```

## logviewer — 本地日志查看器

用于查看本地日志文件。

### 命令行选项

| 选项 | 说明 |
|------|------|
| `-c File` | 配置文件路径（默认 /usr/local/etc/logviewer.ini） |
| `-d` | 调试模式 |

### 配置文件

默认配置文件：`/usr/local/etc/logviewer.ini`

```ini
[www]
logfile = /var/log/www/access.log,/var/log/www/error.log

[nginx]
logdir = /var/log/nginx
```

配置项：
- `logfile` - 指定日志文件路径，多个用逗号分隔
- `logdir` - 指定日志目录，自动遍历目录下所有文件

### 使用方法

```bash
logviewer
```

### 操作流程

1. 启动后显示配置节列表，选择要查看的日志配置
2. 进入文件选择界面，预览窗口显示选中文件的尾部内容
3. 选择要查看的文件
4. 输入关键字正则表达式（可选），过滤日志行
5. 实时显示日志内容，按 Ctrl+C 退出

---

## logviewer.docker — Docker 容器日志查看器

用于查看 Docker 容器日志。

### 命令行选项

| 选项 | 说明 |
|------|------|
| `--host Host` | Docker 主机地址（如 ssh://root@www.netkiller.cn） |
| `-c File` | 配置文件路径（默认 /usr/local/etc/logviewer.ini） |
| `-i User` | 为指定用户安装 logviewer.kubectl 作为登录 Shell |
| `-a User` | 添加用户并设置 logviewer.kubectl 为登录 Shell |
| `-d` | 调试模式 |

### 使用方法

```bash
# 查看本地 Docker 容器
logviewer.docker

# 查看远程 Docker 主机
logviewer.docker --host ssh://root@192.168.1.100
```

### 操作流程

1. 显示当前所有运行中的容器列表
2. 选择要查看日志的容器
3. 输入关键字正则表达式（可选）
4. 实时显示容器日志，按 Ctrl+C 退出

### 功能特点

- 自动列出所有运行中的容器
- 支持远程 Docker 主机（通过 `--host` 指定）
- 默认显示最近 500 行日志
- 支持关键字过滤

---

## logviewer.kubectl — Kubernetes 日志查看器

用于查看 Kubernetes Pod 日志。

### 命令行选项

| 选项 | 说明 |
|------|------|
| `-c File` | kubeconfig 文件路径（默认 ~/.kube/config） |
| `-i User` | 为指定用户安装 logviewer.kubectl 作为登录 Shell |
| `-a User` | 添加用户并设置 logviewer.kubectl 为登录 Shell |
| `-l File` | 日志文件路径（默认 /var/log/logviewer.log） |
| `-d` | 调试模式 |

### 使用方法

```bash
# 使用默认 kubeconfig
logviewer.kubectl

# 指定 kubeconfig 文件
logviewer.kubectl -c /path/to/config
```

### 操作流程

1. **选择 Namespace** - 显示所有命名空间列表
2. **选择 Deployment** - 显示该命名空间下的所有 Deployment
3. **选择 Pod** - 显示该 Deployment 的所有 Pod
4. **查看日志** - 输入关键字正则表达式（可选），实时显示日志

### 功能特点

- 三级导航：Namespace → Deployment → Pod
- 自动过滤非活跃的 Pod
- 默认显示最近 200 行日志
- 支持关键字正则表达式过滤
- 日志记录到 /var/log/logviewer.log

---

## 通用功能

### 关键字搜索

所有版本都支持关键字正则表达式过滤：

```
请输入正则表达式: ERROR|Exception
```

输入正则表达式后，日志将只显示匹配的行，关键字会高亮显示。

### 退出程序

- 按 `Q` 或 `ESC` 退出程序
- 按 `Ctrl+C` 中断日志输出并返回上级菜单

### 交互界面

- `/` 键可快速搜索过滤列表项
- 上下箭头选择选项
- 回车确认选择

---

## 安装为登录 Shell

可以将 logviewer.kubectl 安装为用户登录 Shell，实现用户登录后直接进入日志查看界面：

```bash
# 安装（使用 -i）
logviewer.kubectl -i username

# 添加新用户并安装（使用 -a）
logviewer.kubectl -a newuser
```

这会将用户的登录 Shell 设置为 logviewer.kubectl，用户 SSH 登录后直接进入日志查看流程。

---

## 注意事项

1. 使用 Docker 和 Kubernetes 版本需要相应的环境权限
2. kubectl 需要配置好 kubeconfig 并有相应 namespace 的访问权限
3. Docker 远程连接需要配置好 SSH 免密登录
4. 日志过滤使用 grep 正则表达式，请输入合法的正则语法
