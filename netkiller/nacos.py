#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
##############################################
# Home	: https://wwwnetkiller.cn
# Author: Neo <netkiller@msn.com>
# Data: 2023-03-17
##############################################
import requests

class Nacos():

    def __init__(self, nacos, namespace=None) -> None:
        self.nacos = "{nacos}/nacos/v1".format(nacos=nacos)
        self.namespace = namespace

    def login(self, username, password):
        url = self.nacos + "/auth/login"
        data = {"username": username, "password": password}
        try:
            response = requests.post(url, data)
            if response.status_code == 200:
                self.accessToken = response.json()['accessToken']
                return True
        except requests.exceptions.MissingSchema as err:
            print(err)
            exit(1)
        return False

    def getConfig(self, dataId, group, namespace=None):
        if namespace == None:
            namespace = self.namespace
        url = "{nacos}/cs/configs?accessToken={accessToken}&dataId={dataId}&group={group}&tenant={namespace}".format(
            nacos=self.nacos, accessToken=self.accessToken, dataId=dataId, group=group, namespace=namespace)
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.status_code)
            return (response.text)
        else:
            return None

    def showConfig(self, dataId, group, namespace=None):
        print(self.getConfig(dataId, group, namespace))

    def saveConfig(self, filename, dataId, group, namespace=None):
        file = open(filename, 'w')
        file.write(self.getConfig(dataId, group, namespace))
        file.flush()
        file.close()

    def putConfig(self, filename, dataId, group, namespace=None):
        if namespace == None:
            namespace = self.namespace
        url = "{nacos}/cs/configs?".format(nacos=self.nacos)
        with open(filename) as file:
            content = file.read()
        data = {
            "accessToken": self.accessToken,
            "dataId": dataId,
            "group": group,
            "content": content,
            "tenant": namespace,
            "type": "yaml"
        }

        response = requests.post(url, data)
        if response.status_code == 200:
            return True
        else:
            return False
