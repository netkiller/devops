import os,sys

module = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(module)
sys.path.insert(0,module)

from netkiller.docker import *

image = 'redis:latest'
requirepass='11223344'
environment=['TZ=Asia/Shanghai']

compose = Composes('redis-master-slave')
compose.version('3.9')

master =  Services('master')
master.image(image)
master.container_name('master')
master.restart('always')
master.environment(environment)
master.ports('6379:6379')
master.volumes(['/tmp/master:/data'])
master.sysctls(['net.core.somaxconn=1024'])
master.command([
	'--requirepass '+requirepass,
	'--appendonly yes'])
# master.debug()
# print(master.dump())
compose.services(master)


for i in range(5) :
    slave =  Services('slave-'+str(i))
    slave.image(image).container_name('slave-'+str(i)).restart('always')
    slave.ports(['638{port}:6379'.format(port=i)]).environment(environment)
    slave.volumes(['/tmp/slave{n}:/data'.format(n=i)])
    slave.sysctls(['net.core.somaxconn=1024']).command([
        '--slaveof master 6379',
        '--masterauth '+requirepass,
        '--requirepass ' + requirepass,
        '--appendonly yes'
    ])

    # print(cluster.dump())
    compose.services(slave)

# print (compose.debug())
print(compose.dump())
# compose.save()
# compose.up()