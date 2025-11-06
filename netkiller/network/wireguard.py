# -*- coding: utf-8 -*-
#========================================
# Author: netkiller@msn.com
# Home: https://www.netkiller.cn
# Callsign: BG7NYT
# Data: 2025-10-30
#========================================
import argparse
import subprocess

class Wireguard:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Wireguard config tools',
                                         epilog='Author: netkiller - https://www.netkiller.cn')

        self.parser.add_argument('-c', '--cidr', type=str, default='10.0.0.0/24', metavar="10.0.0.0/24", help='子网')
        self.parser.add_argument('-e', '--endpoint', type=str, default=None, metavar="[服务器公网IP]:50814", help='服务器端IP地址及端口号')
        # self.parser.add_argument('-s','--server', action="store_true", default=False, help='生成服务端配置')
        # self.parser.add_argument('-p','--peer', action="store_true", default=False, help='生成客户端配置')
        self.parser.add_argument('-n','--node', type=int, default=5,  metavar="2", help='指定节点数量并自动创建服务端和客户端配置')

        pass
    def subnet(self, cidr):
        # cidr = "10.660.0.0/24"
        ip_part = cidr.split('/')[0]  # 先取 IP 部分 "10.0.0.0"
        # 按 '.' 分割为列表 ["10", "0", "0", "0"]，取前 3 段拼接并加 '.'
        subnet = '.'.join(ip_part.split('.')[:3]) + '.'
        return (subnet)


    def server(self,cidr:str, keys:dict):
        subnet =self.subnet(cidr)
        address = subnet+'1/24'

        privateKey = keys[0]['private']
        publicKey = keys[0]['public']

        interface = f"""[Interface]
Address = {address}
ListenPort = 51820
PrivateKey = {privateKey}

"""

        peers =[]
        n = 2
        for key in keys[1:]:
            # print(key)
            peerPrivateKey = key['private']
            peerPublicKey = key['public']
            peerAddress = f"{subnet}{n}/32"
            peers.append(f"""[Peer]
PublicKey = {peerPublicKey}
AllowedIPs = {peerAddress}
            """)
            n+=1
        conf = interface + "\n".join(peers)

        with open('wg0.conf','w') as file:
            file.write(conf)
        # print(conf)

    def peer(self,cidr:str, endpoint:str, keys:dict):
        subnet = self.subnet(cidr)
        address = subnet + '1/24'

        privateKey = keys[0]['private']
        publicKey = keys[0]['public']
        peers = []
        n = 2
        for key in keys[1:]:
            # print(key)
            peerPrivateKey = key['private']
            peerPublicKey = key['public']
            peerAddress = f"{subnet}{n}/32"
            conf=f"""[Interface]
PrivateKey = {peerPrivateKey}
Address = {peerAddress}
DNS = 8.8.8.8

[Peer]
PublicKey = {publicKey}
Endpoint = {endpoint}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
                    """

            with open(f'client{n}.conf', 'w') as file:
                file.write(conf)
            n += 1
    def genkey(self, number):
        keys = []
        for n in range():
            privateKey = subprocess.check_output(["wg", "genkey"], encoding="utf-8").strip()
            # print(privateKey)

            publicKey = subprocess.check_output(f"echo '{privateKey}' | wg pubkey", shell=True, encoding="utf-8").strip()
            # print(publicKey)
            keys.append({'private': privateKey, 'public': publicKey})

        # print(keys)
        return keys
    def main(self):
        # (options, args) = self.parser.parse_args()
        args = self.parser.parse_args()
        # print(args)
        # self.parser.print_help()
        #
        if args.cidr and args.endpoint:
            keys = self.genkey(args.node)
            self.server(args.cidr, keys)
            self.peer(args.cidr, args.endpoint, keys)
        else:
            self.parser.print_usage()
            exit()

