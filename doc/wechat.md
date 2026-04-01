# Wechat

企业微信通知

## 安装

### 安装依赖

```bash
pip3 install simple_term_menu prompt_toolkit
```

### 安装 netkiller 库

```bash
pip3 install netkiller
```

## 帮助信息

```
wechat --help
```

```
Usage: wechat [options] message

Options:
  -h, --help            show this help message and exit
  -c FILE, --config=FILE
                        config file (default: /usr/local/etc/wechat.ini)
  -e CORPORATE, --corporate=CORPORATE
                        corporate name (default: default)
  -t TAG, --totag=TAG   tag ID (default: 1)
  -s, --stdin           read message from stdin
  --debug               debug mode

Homepage: https://www.netkiller.cn    Author: Neo <netkiller@msn.com>
```

## 配置企业微信

### 创建企业微信应用

1. 登录企业微信管理后台 (https://work.weixin.qq.com)
2. 进入「应用管理」→「应用」页面
3. 创建应用，保存 `agentid`
4. 设置应用的「接收消息」板块，保存 `secret`
5. 获取企业 ID（`corpid`）：在「我的企业」页面底部查看

### 配置文件

默认配置文件：`/usr/local/etc/wechat.ini`

```ini
[default]
corpid=ww585b1e2860543c3b
secret=xamgd6K_6SOSzyPjTxw9kdqVv7IgePb4zdylgiv6kIc
agentid=1000004

[company2]
corpid=wx1234567890abcdef
secret=another_secret_here
agentid=1000005
```

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `corpid` | 企业 ID |
| `secret` | 应用 secret |
| `agentid` | 应用 agentid |

## 使用方法

### 发送文本消息

```bash
wechat "Hello World"
```

### 指定标签发送

```bash
# 发送给标签 1
wechat -t 1 "告警消息"

# 发送给多个标签（用 | 分隔）
wechat -t "1|2|3" "批量通知"
```

### 切换企业配置

```bash
# 使用 default 配置
wechat -e default "消息"

# 使用其他企业配置
wechat -e company2 "消息"
```

### 从标准输入读取

```bash
# 从管道输入
echo "监控告警" | wechat -s

# 从文件读取
cat /var/log/error.log | wechat -s -t 2
```

### 调试模式

```bash
wechat --debug -t 4 测试消息
```

## 使用示例

### 监控告警

```bash
# CPU 告警
wechat -t 1 "服务器 CPU 使用率超过 90%"

# 磁盘空间告警
wechat -t 2 "磁盘空间不足，当前使用率 95%"
```

### 日志告警

```bash
# 发送错误日志
grep "ERROR" /var/log/app.log | wechat -s -t 3

# 发送最近 10 条告警
tail -10 /var/log/alerts.log | wechat -s -t 1
```

### 部署通知

```bash
# 代码部署完成通知
wechat -t "1|2" "服务部署完成，请确认"
```

## 工作原理

1. 通过 `corpid` 和 `secret` 获取 access_token
2. 使用 access_token 调用企业微信消息发送接口
3. 消息发送到指定的标签（tag）成员

## 注意事项

1. **标签设置** - 确保企业微信应用中已创建相应的标签，并将需要接收消息的成员加入标签
2. **权限要求** - 应用需要具有「发送消息」权限
3. **消息长度** - 企业微信对消息长度有限制，过长消息可能发送失败
4. **token 有效期** - access_token 有效期为 2 小时，脚本每次调用都会重新获取
5. **多企业支持** - 通过 `-e` 参数支持配置多个企业的企业微信
