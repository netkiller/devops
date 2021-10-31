import os,sys
module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,module)

from netkiller.docker import *

service =  Services('nginx')
service.image('nginx:latest')
service.container_name('nginx')
service.restart('always')
service.hostname('www.netkiller.cn')
service.extra_hosts(['db.netkiller.cn:127.0.0.1','cache.netkiller.cn:127.0.0.1','api.netkiller.cn:127.0.0.1'])
service.environment(['TZ=Asia/Shanghai'])
service.ports(['80:80','443:443'])
service.volumes(['/tmp:/tmp'])
service.links('nginx:web1.netkiller.cn')
# service.debug()
# print(service.dump())



for i in range(10) :
    cluster =  Services('nginx-'+str(i))
    cluster.image('nginx:latest').container_name('nginx-'+str(i)).restart('always').hostname('www'+str(i)+'.netkiller.cn')
    cluster.ports(['8{port}:80'.format(port=i)])
    # print(cluster.dump())


compose = Composes('development')
compose.version('3.9')
compose.services(service)
# print (compose.debug())
print(compose.dump())
compose.workdir('/tmp')
compose.save()
# compose.save('/tmp/docker-compost.yaml')