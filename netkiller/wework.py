#! /usr/bin/env python
# -*- coding: UTF-8 -*-
##############################################
# Home	: http://netkiller.github.io
# Author: Neo <netkiller@msn.com>
##############################################

try:
	import requests, sys
	import logging, logging.handlers
	from configparser import ConfigParser
	from optparse import OptionParser, OptionGroup
except ImportError as err:
	print("Error: %s" %(err))

class WeWork():
	def __init__(self, corpid, secret, agentid):
		self.CORPID = corpid
		self.SECRET = secret
		self.AGENTID = agentid
		self.token = None
	def getToken(self):
		url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
		json = {
			"corpid": self.CORPID,
			"corpsecret": self.SECRET
		}
		response = requests.get(url=url, params=json)
		res = response.json()
		if res['errmsg'] == 'ok':
			self.token = res["access_token"]
			return True
		else:
			print(res)
			return False

	def sendMessage(self, json):
		if not self.getToken() :
			return False
		url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % self.token
		response = requests.post(url=url, json=json)
		res = response.json()
		if res['errmsg'] == 'ok':
			return True
		else:
			print(res)
			return False

	def sendTextMessage(self,totag, content):
		data = {
			# "touser": to_user,  # 发送个人填用户账号
			# "toparty": to_user,  # 发送组内成员填部门ID
			"totag": totag,
			"msgtype": "text",
			"agentid": self.AGENTID,
			"text": {"content": content},
			"safe": "0"
		}
		self.sendMessage(json=data)