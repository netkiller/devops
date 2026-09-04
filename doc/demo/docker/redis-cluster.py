from netkiller.docker import *

image = 'redis:latest'
requirepass='11223344'

compose = Composes('redis-master-slave')
compose.version('3.9')

# master =  Services('master')
# master.image(image)
# master.container_name('master')
# master.restart('always')
# master.environment(['TZ=Asia/Shanghai'])
# master.ports('6379:6379')
# master.volumes(['/tmp/master:/data'])
# master.sysctls(['net.core.somaxconn=1024'])
# master.command([
# 	'--requirepass '+requirepass,
# 	'--appendonly yes'])
# # master.debug()
# # print(master.dump())
# compose.services(master)


for i in range(5) :
    slave =  Services('slave-'+str(i))
    slave.image(image).container_name('slave-'+str(i)).restart('always')
    slave.ports(['638{port}:6379'.format(port=i)]).environment(['TZ=Asia/Shanghai'])
    slave.volumes(['/tmp/slave{n}:/data'.format(n=i)])
    slave.sysctls(['net.core.somaxconn=1024']).command([
        '--port 6379',
        '--cluster-enabled yes',
# cluster-config-file nodes-6371.conf
        'cluster-node-timeout 5000'
        '--appendonly yes'
        'protected-mode no',
        '--masterauth '+requirepass,
        '--requirepass ' + requirepass,
        'cluster-announce-ip 10.12.12.10',
         # 这里是宿主机IP
        'cluster-announce-port 6371',
        'cluster-announce-bus-port 16371'
    ])

    # print(cluster.dump())
    compose.services(slave)

# print (compose.debug())
print(compose.dump())
# compose.save()
compose.up()

# compose.save('/tmp/docker-compost.yaml')