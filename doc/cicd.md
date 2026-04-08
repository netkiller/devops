# CICD 操作手册

## 简介

`netkiller/cicd.py` 是一个面向 Kubernetes 的简易 CI/CD 编排器。它负责把单个项目或一组项目串起来执行以下动作：

1. 检出或更新 Git 代码
2. 执行构建命令
3. 构建并推送容器镜像
4. 生成并推送 Nacos 配置
5. 更新 Kubernetes Deployment 镜像

仓库里的实际入口不是 `netkiller/cicd.py`，而是 [`bin/cicd`](/Users/neo/GitHub/devops/bin/cicd)。`bin/cicd` 会先加载外部 `config.py`，再调用 [`netkiller/cicd.py`](/Users/neo/GitHub/devops/netkiller/cicd.py)。

## 适用场景

- Java 或其他可脚本化构建的服务发布
- Docker/Podman 镜像构建与推送
- 基于 Nacos 的配置发布
- 基于 `kubectl set image` 的 Kubernetes 滚动升级

## 执行前准备

运行前建议满足以下条件：

- 在仓库根目录执行 `bin/cicd`
- 已安装 Python 3
- 已安装 `git`
- 已安装 `docker` 或可兼容执行的容器工具
- 已安装 `kubectl`
- 已安装 `nacos` 命令行工具
- 当前机器可以访问 Git 仓库、镜像仓库、Nacos 和 Kubernetes API
- 已准备好 `KUBECONFIG` 或当前环境默认 kubeconfig 可用
- 已准备好构建工具，例如 Maven、Gradle、Node.js 等

### 为什么建议在仓库根目录执行

源码里 `basedir = os.getcwd()`，模板目录和 Nacos 配置目录都是按“当前工作目录”拼出来的：

- `template/DEFAULT_GROUP/<deployment.name>`
- `nacos/DEFAULT_GROUP/<deployment.name>`

如果你不在仓库根目录执行，模板和配置文件路径很容易找错。

## 工作流程

单个项目完整发布时，源码里的执行顺序如下：

1. `init`
2. `checkout`
3. `build`
4. `dockerfile`
5. `nacos`
6. `deploy`

对应行为如下：

### 1. 初始化

初始化阶段会记录日志，并设置一些启动命令。默认会执行：

```bash
alias docker=podman
echo $JAVA_HOME
```

这一步主要是做环境准备和输出调试信息。

### 2. 检出代码

如果工作空间下项目目录已经存在：

- `git fetch`
- `git checkout <branch>`
- `git pull`

如果项目目录不存在：

- `git clone --branch <branch> <url> <project>`

### 3. 执行构建

构建命令来自项目配置里的 `ci.build`。

- 如果定义了 `ci.image`，构建命令会在容器里执行
- 如果没有定义 `ci.image`，构建命令会直接在本机执行

容器模式下会挂载：

- `~/.m2:/root/.m2`
- `~/.gradle:/root/.gradle`
- `<workspace>/<project>:/root/project`
- 临时脚本文件到 `/root/script.sh`

### 4. 构建并推送镜像

镜像标签格式固定为：

```text
<registry>/<project>:<branch>-YYYYMMDD-HHMM
```

随后执行：

```bash
docker build -t <tag> .
docker push <tag>
docker image rm <tag>
```

如果是 `--only image`，还会额外推送 `latest`：

```bash
docker tag <tag> <image>:latest
docker push <image>:latest
docker image rm <image>:latest
```

如果项目配置了 `ci.module`，则会先 `cd` 到该目录，再执行镜像构建。

### 5. 生成并推送 Nacos 配置

这部分有两步：

1. 如果存在模板文件，就先渲染模板
2. 如果目标配置文件存在，就把它推送到 Nacos

其中：

- `dataId = deployment.name`
- `group = DEFAULT_GROUP`
- `namespace = --namespace` 的值

也就是说，当前实现里：

- Nacos `group` 被硬编码为 `DEFAULT_GROUP`
- Nacos `namespace` 和 Kubernetes 命名空间共用同一个参数

### 6. 部署到 Kubernetes

完整发布时，会执行以下命令：

```bash
kubectl set image deployment/<project> <project>=<image> -n <namespace>
kubectl -n <namespace> get deployment/<project> -o wide
kubectl -n <namespace> get pod -o wide | grep <project>
```

这里的 `<project>` 不是 `deployment.name`，而是项目配置字典的键名。通常要求：

- 项目名 = Kubernetes Deployment 名称
- 项目名 = Deployment 中容器名称

否则 `kubectl set image` 这一句会失败。

## 配置说明

`bin/cicd` 会加载一个外部 `config.py`：

```python
from config import *
```

当前仓库没有附带这个 `config.py` 文件，所以你需要自行提供。按照源码，至少要准备以下内容：

- `registry`
- `template`
- `server`
- `username`
- `password`
- `getCofnig(branch)`

### 最小示例

下面这个示例足够让 `bin/cicd` 跑起来：

```python
registry = "harbor.example.com/devops"

template = {
    "SPRING_PROFILES_ACTIVE": "dev",
    "JVM_OPTS": "-Xms512m -Xmx512m"
}

server = "nacos.example.com:8848"
username = "nacos"
password = "secret"

def getCofnig(branch):
    return {
        "user-service": {
            "ci": {
                "url": "git@gitlab.example.com:app/user-service.git",
                "build": [
                    "mvn -U -T 1C clean package -Dmaven.test.skip=true"
                ],
                "module": ".",
                "image": "maven:3.9.6-eclipse-temurin-8"
            },
            "deployment": {
                "group": "backend",
                "name": "user-service.yaml"
            }
        }
    }
```

### 项目配置结构

每个项目至少需要以下字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `ci.url` | 是 | Git 仓库地址 |
| `ci.build` | 是 | 构建命令列表 |
| `ci.module` | 否 | Dockerfile 所在子目录 |
| `ci.image` | 否 | 构建容器镜像，定义后构建命令在容器内运行 |
| `deployment.group` | 是 | 分组名称，供 `--group` 和 `--list` 使用 |
| `deployment.name` | 是 | Nacos 的 `dataId`，也是模板和配置文件名 |

### 模板目录

模板文件位置：

```text
template/DEFAULT_GROUP/<deployment.name>
```

生成后的配置文件位置：

```text
nacos/DEFAULT_GROUP/<deployment.name>
```

模板变量来自 `cd.template(template)` 传入的字典，采用 Python `Template.safe_substitute()` 渲染。

## 命令行参数

源码支持以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n`, `--namespace` | Kubernetes 命名空间，同时也作为 Nacos namespace | `dev` |
| `-w`, `--workspace` | 代码工作空间 | `~/.netkiller/project` |
| `-r`, `--registry` | 镜像仓库地址 | `None` |
| `-u`, `--username` | 镜像仓库用户名 | 无 |
| `-p`, `--password` | 镜像仓库密码 | 无 |
| `-b`, `--branch` | Git 分支 | `master` |
| `-g`, `--group` | 部署组 | 无 |
| `--skip` | 跳过的项目，多个用逗号分隔 | 无 |
| `-o`, `--only` | 只执行某一步 | 无 |
| `--logfile` | 结构化日志文件 | `/tmp/debug.log` |
| `-l`, `--list` | 查看项目列表 | 关闭 |
| `-a`, `--all` | 部署所有项目 | 关闭 |
| `-c`, `--clean` | 清理本地工作目录后再构建 | 关闭 |
| `-s`, `--silent` | 安静模式，把命令输出写入项目日志文件 | 关闭 |
| `--destroy` | 删除整个命名空间 | 关闭 |
| `-d`, `--daemon` | 后台运行 | 关闭 |
| `--parallel` | 并行部署项目数 | 无 |
| `--debug` | 调试模式，日志直接输出到终端 | 关闭 |

### `--only` 支持的值

按源码实际判断，支持以下值：

- `checkout`
- `build`
- `image`
- `nacos`

注意：参数帮助文字里写的是 `images`，但代码实际判断的是 `image`。

这些值的实际行为如下：

- `checkout`：只拉取或更新代码
- `build`：只执行构建命令
- `image`：只构建并推送镜像，同时额外推送 `latest`
- `nacos`：只生成并推送 Nacos 配置，成功后会执行 `kubectl rollout restart deployment/<project> -n <namespace>`

## 常用操作

### 查看项目分组

```bash
bin/cicd --list
```

### 发布单个项目

```bash
bin/cicd -n dev -b master user-service
```

### 发布某个分组

```bash
bin/cicd -n dev -g backend
```

### 发布全部项目

```bash
bin/cicd -n dev --all
```

### 跳过部分项目

```bash
bin/cicd -n dev -g backend --skip user-service,order-service
```

### 仅拉代码

```bash
bin/cicd -n dev -o checkout user-service
```

### 仅执行构建

```bash
bin/cicd -n dev -o build user-service
```

### 仅构建和推送镜像

```bash
bin/cicd -n dev -o image user-service
```

### 仅推送 Nacos 配置

```bash
bin/cicd -n dev -o nacos user-service
```

### 清理工作目录后重新构建

```bash
bin/cicd -n dev -c user-service
```

### 后台部署

```bash
bin/cicd -n dev -g backend -d
```

### 登录镜像仓库后再发布

```bash
bin/cicd -n dev -u robot -p 'secret' user-service
```

## 日志与输出

默认情况下：

- 框架日志写入 `--logfile` 指定文件
- 默认日志文件是 `/tmp/debug.log`

如果启用 `--debug`：

- 日志直接输出到终端
- 不再写入默认日志文件

如果启用 `--silent`：

- 每个项目的命令标准输出和错误输出写入 `<workspace>/<project>.log`

## 特别注意

以下内容不是“建议”，而是从源码直接推出来的实际限制：

### 1. `ci.build` 应该写成列表

建议这样写：

```python
"build": [
    "mvn -U clean package -Dmaven.test.skip=true"
]
```

不要写成单个字符串。当前 `Pipeline.end()` 是按“命令列表”逐条执行的，字符串会被当成字符序列处理。

### 2. `-r/--registry` 当前不完全生效

`bin/cicd` 启动时会先执行：

```python
cd.registry(registry)
```

后续镜像命名和推送用的是 `self.registry`，不是 `options.registry`。因此当前代码里：

- `-r` 主要影响 `docker login`
- 实际镜像推送地址仍然取决于 `config.py` 里的 `registry`

如果你想通过命令行临时切换镜像仓库，当前实现不够完整。

### 3. `--parallel` 存在类型风险

源码里 `--parallel` 没有声明为整数类型，但在分组部署时会直接传给 `multiprocessing.Pool()`。在某些环境里，这个值如果还是字符串，会导致并行部署报错。

### 4. `--all` 固定并发 10

`--all` 模式不会读取 `--parallel`，而是固定：

```python
with Pool(10) as pool:
```

### 5. `--clean` 会直接删除工作目录

执行的是：

```bash
rm -rf <workspace>/<project>
```

如果工作目录里有手工改动，会被直接清掉。

### 6. `--destroy` 会删除整个命名空间

确认输入 `yes` 后会执行：

```bash
kubectl delete namespace <namespace>
```

这是高风险操作。

### 7. Nacos group 被写死为 `DEFAULT_GROUP`

当前版本不能通过参数切换 Nacos group。

### 8. Nacos namespace 和 Kubernetes namespace 共用同一个参数

`--namespace` 同时传给：

- `kubectl -n <namespace>`
- `nacos -n <namespace>`

如果你的 Kubernetes namespace 和 Nacos namespace 不是同一个值，当前脚本不适合直接复用。

### 9. 项目名必须能对应到 Kubernetes Deployment 和容器名

升级镜像使用的是：

```bash
kubectl set image deployment/<project> <project>=<image> -n <namespace>
```

所以项目名必须同时匹配：

- Deployment 名称
- 容器名称

## 建议的使用方式

如果要稳定落地这套脚本，建议按下面方式组织：

1. 在仓库根目录维护 `template/DEFAULT_GROUP/`
2. 在仓库根目录维护 `nacos/DEFAULT_GROUP/`
3. 在独立的 `config.py` 中集中管理 `registry`、Nacos 连接信息和项目清单
4. 每个项目的 `ci.build` 都写成命令列表
5. 项目字典键名直接使用 Kubernetes Deployment 名称
6. 先用 `--only checkout`、`--only build`、`--only image` 分阶段验证，再跑完整发布

## 相关文件

- 入口脚本：[`bin/cicd`](/Users/neo/GitHub/devops/bin/cicd)
- 主逻辑：[`netkiller/cicd.py`](/Users/neo/GitHub/devops/netkiller/cicd.py)
- 执行引擎：[`netkiller/pipeline.py`](/Users/neo/GitHub/devops/netkiller/pipeline.py)
