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
        except requests.exceptions.ConnectionError as err:
            print(err)
            exit(1)
        return False

    def getConfig(self, dataId, group):

        url = "{nacos}/cs/configs?accessToken={accessToken}&dataId={dataId}&group={group}&tenant={namespace}".format(
            nacos=self.nacos, accessToken=self.accessToken, dataId=dataId, group=group, namespace=self.namespace)
        response = requests.get(url)
        if response.status_code == 200:
            return (response.text)
        else:
            return None

    def showConfig(self, dataId, group):
        print(self.getConfig(dataId, group))

    def saveConfig(self, filename, dataId, group):
        config = self.getConfig(dataId, group)
        if config:
            file = open(filename, 'w')
            file.write(config)
            file.flush()
            file.close()

    def putConfig(self, filename, dataId, group, type='yaml'):

        url = "{nacos}/cs/configs?accessToken={accessToken}".format(
            nacos=self.nacos, accessToken=self.accessToken)
        # url = "{nacos}/cs/configs".format(
        # nacos=self.nacos)
        with open(filename) as file:
            content = file.read()
        data = {
            # "accessToken": self.accessToken,
            "tenant": self.namespace,
            "dataId": dataId,
            "group": group,
            "type": type,
            "content": content
        }

        response = requests.post(url, data)
        # print(data, response.text)
        if response.status_code == 200:
            return True
        else:
            return False

    def deleteConfig(self, dataId, group):

        url = "{nacos}/cs/configs?accessToken={accessToken}".format(
            nacos=self.nacos, accessToken=self.accessToken)

        data = {
            # "accessToken": self.accessToken,
            "tenant": self.namespace,
            "dataId": dataId,
            "group": group,
        }

        response = requests.delete(url, data=data)
        # print(url,data, response.text)
        if response.status_code == 200:
            return True
        else:
            return False
