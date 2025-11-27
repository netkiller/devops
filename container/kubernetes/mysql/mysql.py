import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *
namespace = 'default'

config = ConfigMap('mysql')
config.metadata().name('mysql').namespace(namespace).labels({'app': 'mysql'})
config.data({'mysql.cnf': pss('''\
[mysqld]
max_connections=2048
max_execution_time=120
connect_timeout=120
max_allowed_packet=32M
net_read_timeout=120
net_write_timeout=120
# --wait_timeout=60
# --interactive_timeout=60

sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION
character-set-server=utf8mb4
collation-server=utf8mb4_general_ci
explicit_defaults_for_timestamp=true
max_execution_time=0
''')})
config.data({'MYSQL_ROOT_PASSWORD': '123456', 'MYSQL_DATABASE': 'test',
            'MYSQL_USER': 'test', 'MYSQL_PASSWORD': 'test'})
# config.debug()


storageClassName = 'manual'
persistentVolume = PersistentVolume('mysql-pv')
persistentVolume.metadata().name(
    'mysql-pv').labels({'type': 'local'})
persistentVolume.spec().storageClassName(storageClassName)
persistentVolume.spec().capacity({'storage': '2Gi'}).accessModes(
    ['ReadWriteOnce']).hostPath({'path': "/var/lib/mysql"})
persistentVolume.debug()

persistentVolumeClaim = PersistentVolumeClaim('mysql-pvc')
persistentVolumeClaim.metadata().name('mysql-pvc')
persistentVolumeClaim.spec().storageClassName(storageClassName)
persistentVolumeClaim.spec().resources({'requests': {'storage':'2Gi'}})
persistentVolumeClaim.spec().accessModes(
    ['ReadWriteOnce'])
persistentVolumeClaim.debug()
# exit()


statefulSet = StatefulSet()
statefulSet.metadata().name('mysql')
statefulSet.spec().replicas(1)
statefulSet.spec().serviceName('mysql')
statefulSet.spec().selector({'matchLabels': {'app': 'mysql'}})
statefulSet.spec().template().metadata().labels({'app': 'mysql'})
# statefulSet.spec().replicas(1)
# statefulSet.spec().template().spec().securityContext({'sysctls':[{'name':'fs.inotify.max_user_instances', 'value':'4096'}]})
statefulSet.spec().template().spec().initContainers().name('busybox').image('busybox').command(['sh','-c','rm -rf /var/lib/mysql/* && mkdir -p /var/lib/mysql']).volumeMounts([
        {'name': 'data', 'mountPath': '/var/lib/mysql'}])
statefulSet.spec().template().spec().containers().name('mysql').image(
    'mysql:latest'
    # 'mysql:5.7'
    ).ports([{
        'name': 'mysql',
        'protocol': 'TCP',
        'containerPort': 3306
    }]).env([
        {'name': 'MYSQL_ROOT_PASSWORD', 'value': '123456'},
        {'name': 'MYSQL_DATABASE', 'value': 'nacos'},
        {'name': 'MYSQL_USER', 'value': 'nacos'},
        {'name': 'MYSQL_PASSWORD', 'value': 'nacos'}
    ]).volumeMounts([
        {'name': 'config', 'mountPath': '/etc/mysql/conf.d/mysql.cnf',
            'subPath': 'mysql.cnf'},
        {'name': 'data', 'mountPath': '/var/lib/mysql'}
    ]).imagePullPolicy('IfNotPresent')
statefulSet.spec().template().spec().volumes().name(
    'config').configMap({'name': 'mysql'})
statefulSet.spec().template().spec().volumes().name(
    'data').persistentVolumeClaim('mysql-pvc')
# statefulSet.debug()
# exit()

service = Service()
service.metadata().name('mysql')
service.metadata().namespace(namespace).labels({'app': 'mysql'})
service.spec().selector({'app': 'mysql'})
service.spec().type('NodePort')
service.spec().ports([{
    'name': 'mysql',
    'protocol': 'TCP',
    'port': 3306,
    'targetPort': 3306,
    # 'nodePort': 33306
}])

ingress = IngressRouteTCP()
ingress.metadata().name('mysql')
ingress.metadata().namespace(namespace)
ingress.spec().entryPoints(['mysql'])
ingress.spec().routes([{
    'match': 'HostSNI(`*`)',
    'services': [{
        'name': 'mysql',
        'port': 3306
    }]
}])
# ingress.debug()

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(persistentVolume)
compose.add(persistentVolumeClaim)
compose.add(statefulSet)
compose.add(service)
# compose.add(ingress)
compose.debug()
# compose.save()
compose.delete()
compose.create()
