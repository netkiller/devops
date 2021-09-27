#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = 'ww58c3bb58605431e2'  #企业ID，在管理后台获取
        self.CORPSECRET = 'xamgd6K_6SOSv6kIczyPjTxgePb4zdylgiw9kdqVv7I'#自建应用的Secret，每个自建应用里都有单独的secret
        self.AGENTID = '1000004'  #应用ID，在后台应用中获取
        # self.TOUSER = "neo"  # 接收者用户名,多个用户用|分割
        self.TOUSER = '1688850554213993'

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('/tmp/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('/tmp/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('/tmp/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            # "touser": self.TOUSER,
            "totag":"1",
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
                },
            "safe": "0"
            }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json() 
        print(respone)
        return respone["errmsg"]


if __name__ == '__main__':
    wx = WeChat()
    wx.send_data("这是程序发送的第1条消息！\n Python程序调用企业微信API,从自建应用“告警测试应用”发送给管理员的消息！")
    wx.send_data("这是程序发送的第2条消息！")