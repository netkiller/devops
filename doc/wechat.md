# Wechat

企业微信通知

## 安装

    pip3 install -i https://pypi.org/project netkiller-
    
## 帮助信息

    [root@localhost ~]# wechat 
    Usage: wechat [options] message

    Options:
    -h, --help            show this help message and exit
    -c /usr/local/etc/wechat.ini, --config=/usr/local/etc/wechat.ini
                            config file
    -e default, --corporate=default
                            corporate
    -t "1|2|3", --totag="1|2|3"
                            tag
    -s, --stdin           stdin
    --debug               debug mode

    Homepage: https://www.netkiller.cn	Author: Neo <netkiller@msn.com>

## 配置企业微信

    [root@gitlab ~]# cat /usr/local/etc/wechat.ini
    [default]
    corpid=ww585b1e2860543c3b
    secret=xamgd6K_6SOSzyPjTxw9kdqVv7IgePb4zdylgiv6kIc
    agentid=1000004

## 测试

    wechat --debug -t 4 测试

### 标准输入

    [root@localhost ~]# cat /etc/passwd | wechat -t 2 --stdin