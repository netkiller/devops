import os,sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

secret = Secret('tls')
secret.metadata().name('tls').namespace('development')
secret.key('ingress.key').cert('ingress.crt')
secret.type('kubernetes.io/tls')
secret.debug()

print("=" * 40, "Secret", "=" * 40)

secret = Secret('tls')
secret.metadata().name('tls').namespace('development')
secret.data({'tls.crt':'base64 内容','tls.key':'base64 内容'})
secret.type('kubernetes.io/tls')
secret.debug()
# exit()