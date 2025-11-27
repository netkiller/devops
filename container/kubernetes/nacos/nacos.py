import sys
sys.path.insert(0, '/Users/neo/workspace/devops')
from netkiller.kubernetes import *

namespace = 'default'

# namespace = Namespace()
# namespace.metadata().name(namespace)
# namespace.metadata().namespace(namespace)
# namespace.debug()

config = ConfigMap('nacos')
config.apiVersion('v1')
config.metadata().name('nacos').namespace(namespace)
# config.from_file('custom.properties', 'nacos/init.d/custom.properties')
config.data({'application.properties':pss('''\
    # spring
    server.servlet.contextPath=/nacos
    server.contextPath=/nacos
    server.port=8848
    spring.datasource.platform=mysql
    # nacos.cmdb.dumpTaskInterval=3600
    # nacos.cmdb.eventTaskInterval=10
    # nacos.cmdb.labelTaskInterval=300
    # nacos.cmdb.loadDataAtStart=false
    db.num=1
    # db.url.0=jdbc:mysql://mysql-0.mysql:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    # db.url.1=jdbc:mysql://mysql-0.mysql:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    db.url.0=jdbc:mysql://192.168.30.12:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    db.url.1=jdbc:mysql://192.168.30.12:3306/nacos?characterEncoding=utf8&connectTimeout=30000&socketTimeout=30000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8
    # db.url.1=jdbc:mysql://mysql-0.mysql.default.svc.cluster.local:3306/nacos?characterEncoding=utf8&connectTimeout=3000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=Asia/Shanghai
    db.user=nacos
    db.password=nacos
    ### The auth system to use, currently only 'nacos' is supported:
    nacos.core.auth.system.type=nacos


    ### The token expiration in seconds:
    nacos.core.auth.default.token.expire.seconds=${NACOS_AUTH_TOKEN_EXPIRE_SECONDS:18000}

    ### The default token:
    nacos.core.auth.default.token.secret.key=${NACOS_AUTH_TOKEN:SecretKey012345678901234567890123456789012345678901234567890123456789}

    ### Turn on/off caching of auth information. By turning on this switch, the update of auth information would have a 15 seconds delay.
    nacos.core.auth.caching.enabled=${NACOS_AUTH_CACHE_ENABLE:false}
    nacos.core.auth.enable.userAgentAuthWhite=${NACOS_AUTH_USER_AGENT_AUTH_WHITE_ENABLE:false}
    nacos.core.auth.server.identity.key=${NACOS_AUTH_IDENTITY_KEY:serverIdentity}
    nacos.core.auth.server.identity.value=${NACOS_AUTH_IDENTITY_VALUE:security}
    server.tomcat.accesslog.enabled=${TOMCAT_ACCESSLOG_ENABLED:false}
    server.tomcat.accesslog.pattern=%h %l %u %t "%r" %s %b %D
    # default current work dir
    server.tomcat.basedir=
    ## spring security config
    ### turn off security
    nacos.security.ignore.urls=${NACOS_SECURITY_IGNORE_URLS:/,/error,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,/console-fe/public/**,/v1/auth/**,/v1/console/health/**,/actuator/**,/v1/console/server/**}
    # metrics for elastic search
    management.metrics.export.elastic.enabled=false
    management.metrics.export.influx.enabled=false

    nacos.naming.distro.taskDispatchThreadCount=10
    nacos.naming.distro.taskDispatchPeriod=200
    nacos.naming.distro.batchSyncKeyCount=1000
    nacos.naming.distro.initDataRatio=0.9
    nacos.naming.distro.syncRetryDelay=5000
    nacos.naming.data.warmup=true    
'''    
)})
# config.save()
# config.debug()

statefulSet = StatefulSet()
statefulSet.apiVersion('apps/v1')
statefulSet.metadata().name('nacos').labels(
    {'app': 'nacos'}).namespace(namespace)
statefulSet.spec().replicas(3)
statefulSet.spec().serviceName('nacos')
statefulSet.spec().selector({'matchLabels': {'app': 'nacos'}})
statefulSet.spec().template().metadata().labels({'app': 'nacos'})
statefulSet.spec().template().spec().containers().name('nacos').image(
    'nacos/nacos-server:latest').env([
        {'name': 'TZ', 'value': 'Asia/Shanghai'},
        {'name': 'LANG', 'value': 'en_US.UTF-8'},
        {'name': 'PREFER_HOST_MODE', 'value': 'hostname'},
        # {'name': 'MODE', 'value': 'standalone'},
        
        {'name': 'MODE', 'value': 'cluster'},
        {'name': 'NACOS_REPLICAS', 'value': '3'},
        {'name': 'NACOS_SERVERS', 'value': 'nacos-0.nacos.default.svc.cluster.local:8848 nacos-1.nacos.default.svc.cluster.local:8848 nacos-2.nacos.default.svc.cluster.local:8848'},


        {'name': 'SPRING_DATASOURCE_PLATFORM', 'value': 'mysql'},
        # {'name': 'MYSQL_SERVICE_HOST', 'value': 'mysql-0.mysql.default.svc.cluster.local'},
        {'name': 'MYSQL_SERVICE_HOST', 'value': '192.168.30.12'},
        {'name': 'MYSQL_SERVICE_PORT', 'value': '3306'},
        {'name': 'MYSQL_SERVICE_DB_NAME', 'value': 'nacos'},
        {'name': 'MYSQL_SERVICE_USER', 'value': 'nacos'},
        {'name': 'MYSQL_SERVICE_PASSWORD', 'value': 'nacos'},

        # {'name': 'MYSQL_SERVICE_USER', 'value': 'root'},
        # {'name': 'MYSQL_SERVICE_PASSWORD', 'value': 'passw0rd'},
        {'name': 'MYSQL_SERVICE_DB_PARAM', 'value': 'characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&serverTimezone=GMT%2B8'},
        {'name': 'JVM_XMX', 'value': '4g'},
        {'name': 'NACOS_DEBUG', 'value': 'true'},
        {'name': 'TOMCAT_ACCESSLOG_ENABLED', 'value': 'true'},
    ]).ports([
        {'containerPort': 8848},
        {'containerPort': 9848},
        {'containerPort': 9555}
    ]).volumeMounts([
        {'name': 'config', 'mountPath': '/home/nacos/conf/custom.properties', 'subPath': 'custom.properties'},
        # {'name': 'config', 'mountPath': '/home/nacos/conf/application.properties', 'subPath': 'application.properties'}
]).resources({'limits':{'memory': "4Gi"}, 'requests': {'memory': "2Gi"}})
# statefulSet.spec().template().spec().securityContext({'sysctls':[{'name': 'fs.file-max', 'value': '60000'}]})
statefulSet.spec().template().spec().volumes().name('config').configMap({'name': 'nacos'})
statefulSet.debug()
# statefulSet.json()

service = Service()
service.metadata().name('nacos')
service.metadata().namespace(namespace)
service.spec().selector({'app': 'nacos'})
service.spec().type('ClusterIP')
service.spec().ports([
    {'name': 'http', 'protocol': 'TCP', 'port': 8848, 'targetPort': 8848},
    {'name': 'rpc', 'protocol': 'TCP', 'port': 9848, 'targetPort': 9848},
    # {'name': 'http', 'protocol': 'TCP', 'port': 9555, 'targetPort': 9555}
])

print("=" * 40, "Compose", "=" * 40)
compose = Compose('development')
# compose.add(namespace)
compose.add(config)
compose.add(statefulSet)
compose.add(service)
compose.debug()
# compose.save()
# compose.delete()
# compose.create()

print("=" * 40, "Busybox", "=" * 40)
# os.system("sleep 5")
# for cmd in ['kubectl get secret tls', 'kubectl get configmap', 'kubectl get pods', 'kubectl get service', 'kubectl get statefulset', 'kubectl get ingress']:
#     os.system(cmd)
#     print("-" * 50)
