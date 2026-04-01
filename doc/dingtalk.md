钉钉消息推送
===========

## 简介

dingtalk 是一个用于向钉钉群发送消息的工具脚本。通过钉钉自定义机器人 Webhook 接口，可以推送文本和 Markdown 格式的消息。

## 准备工作

### 创建钉钉机器人

1. 打开钉钉群设置
2. 进入「智能群助手」
3. 添加机器人
4. 选择「自定义」机器人
5. 配置机器人名称和安全设置（推荐使用「加签」方式）
6. 复制 `access_token` 和 `secret`

## 使用方法

### 基本语法

```bash
dingtalk [options] message
```

### 命令行选项

| 选项 | 说明 |
|------|------|
| `-t Token` | 设置 access_token（必填） |
| `-s Secret` | 设置密钥（加签模式） |
| `-l File` | 日志文件路径（默认 /var/tmp/dingtalk.log） |
| `--stdin` | 从标准输入读取消息内容 |
| `--text` | 发送文本消息（默认） |
| `--markdown` | 发送 Markdown 格式消息 |
| `--title Title` | Markdown 消息标题 |
| `-d` | 开启调试模式 |

## 使用示例

### 发送文本消息

```bash
dingtalk -t 你的access_token "Hello World"
```

### 发送加签消息

```bash
dingtalk -t 你的access_token -s 你的secret "这是一条加签消息"
```

### 发送 Markdown 消息

```bash
dingtalk -t 你的access_token --markdown --title "标题" "## Markdown 内容"
```

### 从管道读取消息

```bash
echo "消息内容" | dingtalk -t 你的access_token --stdin
```

### 发送日志片段

```bash
tail -20 /var/log/syslog | dingtalk -t 你的access_token --stdin --text
```

## 消息格式

### 文本消息（Text）

普通文本内容，直接显示在聊天窗口。

```
这是一条普通文本消息
```

### Markdown 消息

支持标准 Markdown 格式，适合展示结构化内容。

示例：
```markdown
## 告警通知

- 服务器：web-01
- CPU 使用率：85%
- 内存使用率：90%

> 请及时处理
```

支持的 Markdown 元素：
- 标题（#-######）
- 加粗、斜体
- 链接
- 图片
- 列表
- 引用块
- 代码块

## 日志

默认日志文件：`/var/tmp/dingtalk.log`

日志记录内容：
- 发送的请求数据
- 接口响应结果

## 注意事项

1. **access_token 必填** - 不提供则程序报错退出
2. **加签更安全** - 生产环境建议配合 `-s secret` 使用加签验证
3. **消息长度限制** - 钉钉对消息长度有限制，过长消息可能发送失败
4. **日志权限** - 写入 `/var/tmp/dingtalk.log` 需要相应权限
