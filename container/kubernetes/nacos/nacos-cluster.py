import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *
namespace = 'default'

config = ConfigMap('nacos')
config.apiVersion('v1')
config.metadata().name('nacos').namespace(namespace)
# config.data({
#     'mysql.host': "rm-bp1gna9an26441wsb.mysql.rds.aliyuncs.com",
#     'mysql.port': "3306",
#     'mysql.dbname': "nacos",
#     'mysql.user': "grey",
#     'mysql.password': "A6Diyai1"
# })
config.data({
    'mysql.host': "172.18.200.5",
    'mysql.port': "3306",
    'mysql.dbname': "nacos",
    'mysql.user': "nacos",
    'mysql.password': "nacos"
})
# config.debug()

statefulSet = StatefulSet()
statefulSet = StatefulSet()
statefulSet.apiVersion('apps/v1')
statefulSet.metadata().name('nacos').labels(
    {'app': 'nacos'}).namespace(namespace)
statefulSet.spec().replicas(3)
statefulSet.spec().serviceName('nacos')
statefulSet.spec().selector({'matchLabels': {'app': 'nacos'}})
statefulSet.spec().template().metadata().labels({'app': 'nacos'})
statefulSet.spec().template().metadata().annotations(
    {'pod.alpha.kubernetes.io/initialized': "true"})
# statefulSet.spec().template().spec().affinity().nodeAffinity({
#     'requiredDuringSchedulingIgnoredDuringExecution': [
#         {'labelSelector': {
#             'matchExpressions': [
#                 {'key': 'app',
#                  'operator': 'In',
#                  'values': ['nacos']
#                  }]
#             },
#         'topologyKey': "kubernetes.io/hostname"
#         }
#     ]
# })
statefulSet.spec().template().spec().containers().name('nacos').imagePullPolicy(Define.containers.imagePullPolicy.IfNotPresent).image(
    'nacos/nacos-server:latest').resources(
        # {'requests': {
        # # 'cpu':'200m',
        # 'memory': "2Gi"}}
        ).ports([
        {'name':'client','containerPort': 8848},
        {'name':'client-rpc','containerPort': 9848},
        {'name':'raft-rpc','containerPort': 9849}
    ]).env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'NACOS_REPLICAS', 'value': '1'},
        {'name': 'NACOS_AUTH_ENABLE', 'value': 'true'},
        # {'name': 'SPRING_DATASOURCE_PLATFORM', 'value': 'mysql'},
        
        {'name': 'MYSQL_SERVICE_HOST', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.host'}}},
        {'name': 'MYSQL_SERVICE_PORT', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.port'}}},
        {'name': 'MYSQL_SERVICE_DB_NAME', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.dbname'}}},
        {'name': 'MYSQL_SERVICE_USER', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.user'}}},
        {'name': 'MYSQL_SERVICE_PASSWORD', 'valueFrom':{'configMapKeyRef':{'name': 'nacos','key': 'mysql.password'}}},
        # {'name': 'MYSQL_SERVICE_DB_PARAM', 'value': 'characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8'},
        
        {'name': 'NACOS_SERVER_PORT', 'value': '8848'},
        {'name': 'NACOS_APPLICATION_PORT', 'value': '8848'},
        {'name': 'PREFER_HOST_MODE', 'value': 'hostname'},
        {'name': 'NACOS_SERVERS', 'value': 'nacos-0.nacos.default.svc.cluster.local:8848 nacos-1.nacos.default.svc.cluster.local:8848 nacos-2.nacos.default.svc.cluster.local:8848'},

        # {'name': 'JVM_XMX', 'value': '4g'},
        # {'name': 'NACOS_DEBUG', 'value': 'true'},
        # {'name': 'TOMCAT_ACCESSLOG_ENABLED', 'value': 'true'},
    ])

# statefulSet.debug()

service = Service()
service.metadata().name('nacos')
service.metadata().namespace(namespace)
service.metadata().labels({'app':'nacos'})
service.spec().selector({'app': 'nacos'})
service.spec().type('ClusterIP')
service.spec().ports([
    {'name': 'server', 'protocol': 'TCP', 'port': 8848, 'targetPort': 8848},
    {'name': 'client-rpc', 'protocol': 'TCP', 'port': 9848, 'targetPort': 9848},
    {'name': 'raft-rpc', 'protocol': 'TCP', 'port': 9555, 'targetPort': 9555}
])

# service.debug()

ingress = Ingress()
ingress.apiVersion('networking.k8s.io/v1')
ingress.metadata().name('nacos')
ingress.metadata().namespace(namespace)
# ingress.metadata().annotations({'kubernetes.io/ingress.class': 'nginx'})
ingress.spec().rules([
{
    'host': 'nacos.netkiller.cn',
    'http':{
        'paths': [{
            'pathType': Define.Ingress.pathType.Prefix,
            'path': '/nacos', 
            'backend':{
                'service':{
                    'name':'nacos', 
                    'port':{'number': 8848}
                }
            }}]}
}
])
# ingress.debug()

kubeconfig =  os.path.expanduser('~/workspace/ops/ensd/k3s.yaml')
# kubeconfig =  os.path.expanduser('~/tmp/ops/ensd/k3d-test.yaml')
# kubeconfig = '/Volumes/Data/kubeconfig'
kubernetes = Kubernetes(kubeconfig)
compose = Compose('nacos')
compose.add(config)
compose.add(statefulSet)
compose.add(service)
compose.add(ingress)
kubernetes.compose(compose)
kubernetes.main()
