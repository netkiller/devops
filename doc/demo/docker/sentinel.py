from netkiller.docker import *

image = 'redis:latest'
requirepass='11223344'

compose = Composes('redis-master-slave')
compose.version('3.9')

master =  Services('master')
master.image(image)
master.container_name('master')
master.restart('always')
master.environment(['TZ=Asia/Shanghai'])
master.ports('6379:6379')
master.volumes(['/tmp/master:/data'])
master.sysctls(['net.core.somaxconn=1024'])
master.command([
	'--requirepass '+requirepass,
	'--appendonly yes'])
# master.debug()
# print(master.dump())
compose.services(master)


with open("sentinel.conf","w") as file:
    file.write(
        '''
#port 6379
dir /tmp
sentinel monitor mymaster 172.19.0.3 6379 2
sentinel down-after-milliseconds mymaster 30000
sentinel parallel-syncs mymaster 1
sentinel auth-pass mymaster redispwd
sentinel failover-timeout mymaster 180000
sentinel deny-scripts-reconfig yes
        '''
    )

for i in range(5) :
    name = 'sentinel-'+str(i)
    slave =  Services(name)
    slave.image(image).container_name(name).restart('always')
    slave.ports(['638{port}:6379'.format(port=i)]).environment(['TZ=Asia/Shanghai'])
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
compose.up()

# compose.save('/tmp/docker-compost.yaml')