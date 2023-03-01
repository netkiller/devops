#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: https://www.netkiller.cn
# Author: Neo <netkiller@msn.com>
# Help  : https://github.com/netkiller/devops/blob/master/doc/zentao.md
##############################################

import requests

# url = 'http://172.18.200.10/zentao/api.php/v1'
url = 'http://172.18.200.10/api.php'


class Zentao():
	def __init__(self) -> None:
		pass

	def token(self):
		# headers = {"content-type": "application/json"}
		data = {"account": "test", "password": "Qwe123"}
		# data = json.dumps(json)
		request = requests.post(url + '/tokens', json=data)        # , headers=headers
		print(request)
		print(request.text)

	def main(self):
		pass


# print(request.text)
# print(json.loads(request.content.decode()))
# try:
#     json_string = request.json()
#     if json_string['status'] == 'success':
#         data = json.loads(json_string['data'])
#         value = data['title']
# except requests.exceptions.JSONDecodeError:
#     value = None
# return (value)
zentao = Zentao()
zentao.token()
