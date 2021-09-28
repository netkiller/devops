# Voice 

    Usage: voice [options] message

    Options:
    -h, --help            show this help message and exit
    --config=/usr/local/etc/notification.ini
                            config file
    --debug               debug mode

    Subscribe:
        -d, --daemon        run as daemon

    Publish:
        -c notification, --channel=notification
                            pubsub channel

    Homepage: http://www.netkiller.cn       Author: Neo <netkiller@msn.com>

## 配置 Redis

    vim /usr/local/etc/notification.ini

    [redis]
    ;host=127.0.0.1
    host=192.168.30.5
    port=6379
    db=5
    password=
    channel=notification

## 启动播报端

    neo@MacBook-Pro-Neo ~ % voice -d

    # 指定配置文件
    neo@MacBook-Pro-Neo ~ % voice --config=etc/notification.ini

## 发布通知

    neo@MacBook-Pro-Neo ~ % bin/voice 开发环境升级完成

    # 指定配置文件
    neo@MacBook-Pro-Neo ~ % bin/voice --config=etc/notification.ini 测试环境升级完成

    # 指定播报频道
    neo@MacBook-Pro-Neo ~ % bin/voice -c office --config=etc/notification.ini 测试环境升级完成